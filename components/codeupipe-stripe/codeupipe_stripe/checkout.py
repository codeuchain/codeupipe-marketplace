"""StripeCheckout — create Stripe Checkout sessions."""


class StripeCheckout:
    """Create a Stripe Checkout session from payload data.

    Reads:
        - ``api_key``: Stripe secret key (or passed at init).
        - ``price_id``: Stripe Price ID.
        - ``success_url``: Redirect URL on success.
        - ``cancel_url``: Redirect URL on cancel (optional).

    Writes:
        - ``checkout_url``: The Checkout session URL.
        - ``checkout_session_id``: The session ID.
    """

    def __init__(self, api_key: str = ""):
        self._api_key = api_key

    def call(self, payload):
        import stripe

        stripe.api_key = self._api_key or payload.get("api_key")
        session = stripe.checkout.Session.create(
            mode="payment",
            line_items=[{"price": payload.get("price_id"), "quantity": 1}],
            success_url=payload.get("success_url") or "https://example.com/success",
            cancel_url=payload.get("cancel_url") or "https://example.com/cancel",
        )
        return payload.insert("checkout_url", session.url).insert(
            "checkout_session_id", session.id
        )
