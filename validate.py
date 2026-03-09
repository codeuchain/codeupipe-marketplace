#!/usr/bin/env python3
"""
Validate marketplace manifests and rebuild index.json.

Usage:
    python validate.py              # Validate all manifests
    python validate.py --build      # Validate + rebuild index.json
    python validate.py --check      # Validate + check index.json is up-to-date

Zero external dependencies — stdlib only.
"""

import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).parent
COMPONENTS_DIR = ROOT / "components"
INDEX_FILE = ROOT / "index.json"
SCHEMA_FILE = ROOT / "schema.json"

# ── Validation rules (no jsonschema dependency) ──────────────────

REQUIRED_FIELDS = [
    "name", "provider", "type", "repo", "description",
    "categories", "filters", "trust", "min_codeupipe", "latest",
    "author", "license",
]

VALID_TYPES = {"connector", "filter", "hook", "bundle"}
VALID_TRUST = {"verified", "community"}
NAME_PATTERN = re.compile(r"^codeupipe-[a-z0-9][a-z0-9-]*$")
PROVIDER_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SEMVER_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
CATEGORY_PATTERN = re.compile(r"^[a-z0-9-]+$")
FILTER_PATTERN = re.compile(r"^[A-Z][a-zA-Z0-9]*$")


def validate_manifest(path: Path) -> list[str]:
    """Validate a single manifest.json. Returns list of error strings."""
    errors: list[str] = []
    label = str(path.relative_to(ROOT))

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{label}: Invalid JSON — {exc}"]

    if not isinstance(data, dict):
        return [f"{label}: Top-level must be a JSON object"]

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{label}: Missing required field '{field}'")

    if errors:
        return errors  # Can't validate further without required fields

    # Name format
    if not NAME_PATTERN.match(data["name"]):
        errors.append(
            f"{label}: 'name' must match codeupipe-[a-z0-9-]+ "
            f"(got {data['name']!r})"
        )

    # Name matches directory
    expected_dir = data["name"]
    actual_dir = path.parent.name
    if actual_dir != expected_dir:
        errors.append(
            f"{label}: Directory name '{actual_dir}' doesn't match "
            f"package name '{expected_dir}'"
        )

    # Provider format
    if not PROVIDER_PATTERN.match(data["provider"]):
        errors.append(
            f"{label}: 'provider' must be lowercase alphanumeric + hyphens "
            f"(got {data['provider']!r})"
        )

    # Type
    if data["type"] not in VALID_TYPES:
        errors.append(
            f"{label}: 'type' must be one of {sorted(VALID_TYPES)} "
            f"(got {data['type']!r})"
        )

    # Trust
    if data["trust"] not in VALID_TRUST:
        errors.append(
            f"{label}: 'trust' must be one of {sorted(VALID_TRUST)} "
            f"(got {data['trust']!r})"
        )

    # Semver fields
    for field in ("min_codeupipe", "latest"):
        if not SEMVER_PATTERN.match(data[field]):
            errors.append(
                f"{label}: '{field}' must be semver X.Y.Z "
                f"(got {data[field]!r})"
            )

    # Categories — must be non-empty list of lowercase strings
    cats = data["categories"]
    if not isinstance(cats, list) or len(cats) == 0:
        errors.append(f"{label}: 'categories' must be a non-empty list")
    elif not all(isinstance(c, str) and CATEGORY_PATTERN.match(c) for c in cats):
        errors.append(
            f"{label}: 'categories' entries must be lowercase alphanumeric + hyphens"
        )

    # Filters — list of PascalCase strings
    filters = data["filters"]
    if not isinstance(filters, list):
        errors.append(f"{label}: 'filters' must be a list")
    elif not all(isinstance(f, str) and FILTER_PATTERN.match(f) for f in filters):
        errors.append(
            f"{label}: 'filters' entries must be PascalCase class names"
        )

    # Description length
    if len(data["description"]) > 200:
        errors.append(
            f"{label}: 'description' exceeds 200 characters "
            f"({len(data['description'])})"
        )

    # Repo URL format (basic check)
    if not data["repo"].startswith("https://"):
        errors.append(f"{label}: 'repo' must be an HTTPS URL")

    return errors


def discover_manifests() -> list[Path]:
    """Find all manifest.json files under components/."""
    if not COMPONENTS_DIR.exists():
        return []
    manifests = sorted(COMPONENTS_DIR.glob("*/manifest.json"))
    return manifests


def build_index(manifests: list[Path]) -> dict:
    """Build the index.json structure from validated manifests."""
    connectors = []
    for path in manifests:
        data = json.loads(path.read_text(encoding="utf-8"))
        connectors.append(data)

    # Sort by name for stable output
    connectors.sort(key=lambda c: c["name"])

    return {
        "version": 1,
        "updated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "connectors": connectors,
    }


def main() -> int:
    build = "--build" in sys.argv
    check = "--check" in sys.argv

    manifests = discover_manifests()

    if not manifests:
        print("⚠  No manifests found in components/")
        return 0

    print(f"Validating {len(manifests)} manifest(s)...\n")

    all_errors: list[str] = []
    seen_names: set[str] = set()

    for path in manifests:
        errors = validate_manifest(path)
        all_errors.extend(errors)

        if not errors:
            data = json.loads(path.read_text(encoding="utf-8"))
            name = data["name"]
            if name in seen_names:
                all_errors.append(
                    f"Duplicate package name: '{name}' appears in multiple manifests"
                )
            seen_names.add(name)
            print(f"  ✅ {path.parent.name}")
        else:
            for err in errors:
                print(f"  ❌ {err}")

    print()

    if all_errors:
        print(f"FAILED — {len(all_errors)} error(s)")
        return 1

    print(f"All {len(manifests)} manifest(s) valid.\n")

    if build:
        index = build_index(manifests)
        INDEX_FILE.write_text(
            json.dumps(index, indent=2) + "\n", encoding="utf-8"
        )
        print(f"✅ index.json rebuilt ({len(index['connectors'])} components)")
        return 0

    if check:
        index = build_index(manifests)
        # Compare with current index (ignore 'updated' timestamp)
        if INDEX_FILE.exists():
            current = json.loads(INDEX_FILE.read_text(encoding="utf-8"))
            # Normalize: strip 'updated' for comparison
            current_cmp = {k: v for k, v in current.items() if k != "updated"}
            new_cmp = {k: v for k, v in index.items() if k != "updated"}
            if json.dumps(current_cmp, sort_keys=True) == json.dumps(new_cmp, sort_keys=True):
                print("✅ index.json is up-to-date")
                return 0
            else:
                print("❌ index.json is out-of-date — run: python validate.py --build")
                return 1
        else:
            print("❌ index.json does not exist — run: python validate.py --build")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
