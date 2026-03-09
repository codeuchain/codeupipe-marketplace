"""ResendTemplate — render and send templated emails via Resend."""


class ResendTemplate:
    """Send a templated email using Resend.

    Reads: ``from_email``, ``to``, ``subject``, ``template`` (HTML with {placeholders}),
           ``template_data`` (dict of placeholder values), ``api_key``.
    Writes: ``email_id``.
    """

    def __init__(self, api_key: str = ""):
        self._api_key = api_key

    def call(self, payload):
        import resend

        resend.api_key = self._api_key or payload.get("api_key")

        template = payload.get("template") or ""
        data = payload.get("template_data") or {}
        html = template.format(**data)

        params = {
            "from": payload.get("from_email"),
            "to": payload.get("to"),
            "subject": payload.get("subject"),
            "html": html,
        }

        result = resend.Emails.send(params)
        return payload.insert("email_id", result["id"])
