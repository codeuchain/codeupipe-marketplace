"""StripeCustomer — create and manage Stripe customers."""


class StripeCustomer:
    """Create or retrieve a Stripe Customer.

    Reads:
        - ``api_key``: Stripe secret key (or passed at init).
        - ``email``: Customer email.
        - ``name``: Customer name (optional).

    Writes:
        - ``customer_id``: The Stripe Customer ID.
    """

    def __init__(self, api_key: str = ""):
        self._api_key = api_key

    def call(self, payload):
        import stripe

        stripe.api_key = self._api_key or payload.get("api_key")
        customer = stripe.Customer.create(
            email=payload.get("email"),
            name=payload.get("name") or None,
        )
        return payload.insert("customer_id", customer.id)
