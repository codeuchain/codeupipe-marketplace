"""ResendEmail — send transactional emails via Resend."""


class ResendEmail:
    """Send an email using the Resend API.

    Reads: ``from_email``, ``to``, ``subject``, ``html`` (or ``text``), ``api_key``.
    Writes: ``email_id``.
    """

    def __init__(self, api_key: str = ""):
        self._api_key = api_key

    def call(self, payload):
        import resend

        resend.api_key = self._api_key or payload.get("api_key")
        params = {
            "from": payload.get("from_email"),
            "to": payload.get("to"),
            "subject": payload.get("subject"),
        }
        html = payload.get("html")
        text = payload.get("text")
        if html:
            params["html"] = html
        elif text:
            params["text"] = text

        result = resend.Emails.send(params)
        return payload.insert("email_id", result["id"])
