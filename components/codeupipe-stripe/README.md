# codeupipe-stripe

Stripe checkout, subscriptions, webhooks, and customer management for codeupipe pipelines.

## Install

```bash
cup marketplace install codeupipe-stripe
```

## Filters

| Filter | Description |
|--------|-------------|
| `StripeCheckout` | Create Stripe Checkout sessions |
| `StripeSubscription` | Manage subscriptions |
| `StripeWebhook` | Verify and process Stripe webhooks |
| `StripeCustomer` | Create and manage customers |

## Usage

```python
from codeupipe import Payload, Pipeline
from codeupipe_stripe import StripeCheckout

pipeline = Pipeline()
pipeline.add_filter(StripeCheckout(api_key="sk_test_..."), name="checkout")

result = await pipeline.run(Payload({
    "price_id": "price_xxx",
    "success_url": "https://example.com/success",
}))
```
