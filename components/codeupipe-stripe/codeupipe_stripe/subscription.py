"""StripeSubscription — manage Stripe subscriptions."""


class StripeSubscription:
    """Create or retrieve a Stripe Subscription.

    Reads:
        - ``api_key``: Stripe secret key (or passed at init).
        - ``customer_id``: Stripe Customer ID.
        - ``price_id``: Stripe Price ID.

    Writes:
        - ``subscription_id``: The created subscription ID.
        - ``subscription_status``: Current status.
    """

    def __init__(self, api_key: str = ""):
        self._api_key = api_key

    def call(self, payload):
        import stripe

        stripe.api_key = self._api_key or payload.get("api_key")
        sub = stripe.Subscription.create(
            customer=payload.get("customer_id"),
            items=[{"price": payload.get("price_id")}],
        )
        return payload.insert("subscription_id", sub.id).insert(
            "subscription_status", sub.status
        )
