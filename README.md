# codeupipe Marketplace

Community-driven index for [codeupipe](https://github.com/codeuchain/codeupipe) connectors and components.

This repo is **the** registry. Packages are hosted on PyPI — this is the discovery layer that lets `cup marketplace search` find them.

🌐 **[Browse the Marketplace →](https://codeuchain.github.io/codeupipe-marketplace/)** — search, filter, and explore all available components from your browser.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│  codeupipe-marketplace (this repo)                              │
│                                                                 │
│  components/                    index.json                      │
│  ├── codeupipe-stripe/          ┌──────────────────────┐        │
│  │   └── manifest.json  ──►    │ Built automatically   │        │
│  ├── codeupipe-google-ai/      │ from all manifests    │        │
│  │   └── manifest.json  ──►    │ on merge to main      │        │
│  └── your-package/              └─────────┬────────────┘        │
│      └── manifest.json  ──►              │                      │
│                                           ▼                     │
│                              Raw GitHub URL fetched              │
│                              by `cup marketplace` CLI            │
└─────────────────────────────────────────────────────────────────┘
```

## For Users

```bash
# Search for connectors
cup marketplace search "payments"
# → codeupipe-stripe ✅ (v0.2.1) — Checkout, Subscriptions, Webhooks

# Get details
cup marketplace info codeupipe-stripe

# Install (convenience wrapper around pip)
cup marketplace install codeupipe-stripe
```

No ceremony. The connector self-registers via Python entry points. After `pip install`, it's immediately available in your pipelines via `cup connect --list`.

## For Component Authors

Want to publish a connector or component? **Fork → add manifest → PR.** That's it.

### Quick Start

1. **Build your package** — follow the [connector guide](https://github.com/codeuchain/codeupipe/blob/main/docs/ring8-connect-blueprint.md)
2. **Publish to PyPI** — `pip install your-package` must work
3. **Fork this repo**
4. **Copy the template**: `cp -r _template components/your-package-name`
5. **Fill in `manifest.json`** with your package metadata
6. **Open a PR**

CI validates your manifest automatically. Once merged, your component appears in `cup marketplace search` within minutes.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

## Trust Tiers

| Tier | Badge | Meaning |
|------|-------|---------|
| **verified** | ✅ | Published by codeuchain org, reviewed and tested |
| **community** | 🔷 | Community-submitted, CI-validated |
| **unindexed** | — | Works via entry points but not registered here |

All tiers work with `cup connect --list`. The marketplace only affects discoverability — not functionality.

## Component Types

| Type | Description | Example |
|------|-------------|---------|
| `connector` | Wraps an external service (API, DB, etc.) | codeupipe-stripe |
| `filter` | Reusable processing filter | codeupipe-nlp-filters |
| `hook` | Lifecycle hook (logging, metrics, etc.) | codeupipe-datadog |
| `bundle` | Pre-composed pipeline bundle | codeupipe-etl-starter |

## Index Schema

Every component has a `manifest.json`:

```json
{
  "name": "codeupipe-example",
  "provider": "example",
  "type": "connector",
  "repo": "https://github.com/codeuchain/codeupipe-marketplace",
  "description": "One-line description of what this does",
  "categories": ["category1", "category2"],
  "filters": ["FilterName1", "FilterName2"],
  "trust": "community",
  "min_codeupipe": "0.8.0",
  "latest": "0.1.0",
  "author": "Your Name",
  "license": "Apache-2.0"
}
```

## Links

- **Browse online**: [codeuchain.github.io/codeupipe-marketplace](https://codeuchain.github.io/codeupipe-marketplace/)
- **Core framework**: [codeuchain/codeupipe](https://github.com/codeuchain/codeupipe)
- **Documentation**: [codeupipe.com](https://codeupipe.com)
- **Connector guide**: [Ring 8 Blueprint](https://github.com/codeuchain/codeupipe/blob/main/docs/ring8-connect-blueprint.md)

## License

Apache-2.0 — same as codeupipe core.
