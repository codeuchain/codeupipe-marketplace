"""StripeWebhook — verify and process Stripe webhook events."""


class StripeWebhook:
    """Verify a Stripe webhook signature and extract the event.

    Reads:
        - ``webhook_secret``: Stripe webhook endpoint secret (or passed at init).
        - ``webhook_payload``: Raw request body (bytes or str).
        - ``webhook_signature``: Stripe-Signature header value.

    Writes:
        - ``event_type``: e.g. 'checkout.session.completed'.
        - ``event_data``: The event data object.
        - ``event_id``: Stripe event ID.
    """

    def __init__(self, webhook_secret: str = ""):
        self._secret = webhook_secret

    def call(self, payload):
        import stripe

        secret = self._secret or payload.get("webhook_secret")
        body = payload.get("webhook_payload")
        sig = payload.get("webhook_signature")

        event = stripe.Webhook.construct_event(body, sig, secret)
        return (
            payload.insert("event_type", event["type"])
            .insert("event_data", event["data"]["object"])
            .insert("event_id", event["id"])
        )
