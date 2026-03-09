#!/usr/bin/env python3
"""Build contributors.json from git history of component manifests.

Runs at deploy time (CI) to extract per-component contributor data:
- Who created the manifest (original author)
- Who has modified it (all contributors)
- Commit timeline with messages

Output: site/contributors.json consumed by the marketplace SPA.

Usage:
    python3 build_contributors.py              # writes site/contributors.json
    python3 build_contributors.py --pretty     # human-readable output
"""

import json
import os
import subprocess
import sys
from pathlib import Path


def git(*args: str) -> str:
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        cwd=str(ROOT),
    )
    return result.stdout.strip()


def get_component_dirs() -> list:
    """Find all component directories with a manifest.json."""
    components_dir = ROOT / "components"
    if not components_dir.exists():
        return []
    dirs = []
    for child in sorted(components_dir.iterdir()):
        manifest = child / "manifest.json"
        if child.is_dir() and manifest.exists():
            dirs.append(child)
    return dirs


def extract_log(manifest_path: str) -> list:
    """Extract git log for a file: hash, author, email, date, message."""
    raw = git(
        "log",
        "--follow",
        "--format=%H|%an|%ae|%aI|%s",
        "--",
        manifest_path,
    )
    if not raw:
        return []

    commits = []
    for line in raw.splitlines():
        parts = line.split("|", 4)
        if len(parts) < 5:
            continue
        commits.append({
            "sha": parts[0],
            "author": parts[1],
            "email": parts[2],
            "date": parts[3],
            "message": parts[4],
        })
    return commits


def github_avatar(email: str, author: str) -> str:
    """Best-effort GitHub avatar URL from email or author name.

    GitHub noreply emails contain the username:
        12345678+username@users.noreply.github.com
    For bot commits we use the bot avatar.
    Otherwise fall back to gravatar via GitHub's identicon service.
    """
    if "noreply.github.com" in email:
        # Extract username from GitHub noreply email
        # Format: 12345678+username@users.noreply.github.com
        # or:     username@users.noreply.github.com
        local = email.split("@")[0]
        if "+" in local:
            username = local.split("+", 1)[1]
        else:
            username = local
        return f"https://github.com/{username}.png?size=40"

    if email == "github-actions[bot]@users.noreply.github.com":
        return "https://github.com/github-actions%5Bbot%5D.png?size=40"

    # Fall back to GitHub's avatar-by-email endpoint (works for public emails)
    # If that fails in the browser, the SPA handles it with a fallback initial
    return f"https://avatars.githubusercontent.com/u/e?email={email}&s=40"


def build_component_data(comp_dir: Path) -> dict:
    """Build contributor data for one component."""
    name = comp_dir.name
    manifest_rel = f"components/{name}/manifest.json"

    commits = extract_log(manifest_rel)
    if not commits:
        return {
            "name": name,
            "contributors": [],
            "commits": [],
            "created_by": None,
            "created_at": None,
        }

    # Deduplicate contributors by email, preserve order (most recent first)
    seen_emails = set()
    contributors = []
    for c in commits:
        if c["email"] not in seen_emails:
            seen_emails.add(c["email"])
            contributors.append({
                "name": c["author"],
                "email": c["email"],
                "avatar": github_avatar(c["email"], c["author"]),
            })

    # Original author = last commit in history (oldest)
    oldest = commits[-1]
    created_by = {
        "name": oldest["author"],
        "email": oldest["email"],
        "avatar": github_avatar(oldest["email"], oldest["author"]),
    }

    return {
        "name": name,
        "created_by": created_by,
        "created_at": oldest["date"],
        "contributors": contributors,
        "commits": [
            {
                "sha": c["sha"][:7],
                "sha_full": c["sha"],
                "author": c["author"],
                "email": c["email"],
                "avatar": github_avatar(c["email"], c["author"]),
                "date": c["date"],
                "message": c["message"],
            }
            for c in commits
        ],
    }


def main():
    pretty = "--pretty" in sys.argv

    comp_dirs = get_component_dirs()
    if not comp_dirs:
        print("  [contributors] No component directories found")
        return

    result = {}
    for comp_dir in comp_dirs:
        data = build_component_data(comp_dir)
        result[data["name"]] = data
        n_contributors = len(data["contributors"])
        n_commits = len(data["commits"])
        print(f"  [contributors] {data['name']}: {n_contributors} contributor(s), {n_commits} commit(s)")

    # Write output
    out_path = ROOT / "site" / "contributors.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(result, indent=2 if pretty else None, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"  [contributors] → {out_path.relative_to(ROOT)} ({len(result)} components)")


ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    main()
