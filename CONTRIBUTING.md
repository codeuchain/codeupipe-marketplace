# Contributing to the codeupipe Marketplace

Thanks for sharing your component with the community! This guide walks you through the process.

## Prerequisites

1. **A working codeupipe component** — a Python package with `codeupipe.connectors` entry points
2. **Published on PyPI** — `pip install your-package` must work
3. **A GitHub repo** — so users can file issues and see source code

## Step-by-Step

### 1. Fork This Repo

Click **Fork** on GitHub, then clone your fork:

```bash
git clone https://github.com/YOUR-USERNAME/codeupipe-marketplace.git
cd codeupipe-marketplace
```

### 2. Create Your Component Directory

```bash
cp -r _template components/your-package-name
```

For example:
```bash
cp -r _template components/codeupipe-twilio
```

### 3. Fill In Your Manifest

Edit `components/your-package-name/manifest.json`:

```json
{
  "name": "codeupipe-twilio",
  "provider": "twilio",
  "type": "connector",
  "repo": "https://github.com/codeuchain/codeupipe-marketplace",
  "description": "Twilio SMS, voice, and messaging for codeupipe pipelines",
  "categories": ["communications", "sms", "voice"],
  "filters": ["TwilioSendSMS", "TwilioMakeCall"],
  "trust": "community",
  "min_codeupipe": "0.8.0",
  "latest": "1.0.0",
  "author": "Your Name",
  "license": "Apache-2.0"
}
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | ✅ | Package name (must start with `codeupipe-`) |
| `provider` | ✅ | Short provider identifier (e.g., `stripe`, `twilio`) |
| `type` | ✅ | One of: `connector`, `filter`, `hook`, `bundle` |
| `repo` | ✅ | Always `https://github.com/codeuchain/codeupipe-marketplace` |
| `description` | ✅ | One-line description (< 120 chars) |
| `categories` | ✅ | List of category tags (lowercase, hyphenated) |
| `filters` | ✅ | List of exported Filter/StreamFilter class names |
| `trust` | ✅ | `"community"` for community submissions |
| `min_codeupipe` | ✅ | Minimum codeupipe version required |
| `latest` | ✅ | Latest published version |
| `author` | ✅ | Author or organization name |
| `license` | ✅ | `Apache-2.0` (all marketplace components) |

### 4. Validate Locally

Run the validation script to catch issues before pushing:

```bash
python validate.py
```

This checks:
- JSON syntax
- Required fields present
- Package name format (`codeupipe-*`)
- Type is valid
- Trust tier is valid
- No duplicate entries

### 5. Commit and Push

```bash
git checkout -b add-codeupipe-twilio
git add components/codeupipe-twilio/manifest.json
git commit -m "Add codeupipe-twilio connector"
git push origin add-codeupipe-twilio
```

### 6. Open a Pull Request

Open a PR against `codeuchain/codeupipe-marketplace:main`. CI will validate your manifest automatically. Fill in the PR template — it asks for:

- What your component does
- Link to your repo
- A quick usage example

### 7. Review & Merge

A maintainer reviews the PR. Once merged:
- CI rebuilds `index.json` from all manifests
- Your component is discoverable via `cup marketplace search` within minutes

## Updating Your Component

When you release a new version:

1. Update `latest` in your `manifest.json`
2. Update any new `filters` you've added
3. Open a PR with the changes

## Trust Tiers

| Tier | Who | How |
|------|-----|-----|
| `verified` | codeuchain org packages | Set by maintainers only |
| `community` | Everyone else | Default for all PRs |

Community components are **not** second-class. They show up in search results with a 🔷 badge. Verification is a signal of provenance, not quality.

## Component Types

- **`connector`** — Wraps an external service (API, database, etc.)
- **`filter`** — Reusable processing filter for common tasks
- **`hook`** — Lifecycle hook (logging, metrics, monitoring)
- **`bundle`** — Pre-composed pipeline template / starter kit

## Guidelines

1. **One manifest per package.** Don't bundle multiple packages in one PR.
2. **Package name must start with `codeupipe-`.** This is the namespace convention.
3. **Keep descriptions concise.** Under 120 characters.
4. **Categories are lowercase.** Use hyphens for multi-word: `google-ai`, not `Google AI`.
5. **Don't modify other components' manifests** in your PR.
6. **Don't modify `index.json` directly.** It's built automatically from manifests.

## Questions?

- Open an [issue](https://github.com/codeuchain/codeupipe-marketplace/issues)
- Ask in the [codeupipe discussions](https://github.com/codeuchain/codeupipe/discussions)
