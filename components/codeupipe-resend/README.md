# codeupipe-resend

Resend transactional email and template rendering for codeupipe pipelines.

## Install

```bash
cup marketplace install codeupipe-resend
```

## Filters

| Filter | Description |
|--------|-------------|
| `ResendEmail` | Send transactional emails via Resend |
| `ResendTemplate` | Render and send templated emails |

## Usage

```python
from codeupipe import Payload, Pipeline
from codeupipe_resend import ResendEmail

pipeline = Pipeline()
pipeline.add_filter(ResendEmail(api_key="re_..."), name="send")

result = await pipeline.run(Payload({
    "from_email": "hello@example.com",
    "to": "user@example.com",
    "subject": "Welcome!",
    "html": "<h1>Welcome to our app</h1>",
}))
print(result.get("email_id"))
```
