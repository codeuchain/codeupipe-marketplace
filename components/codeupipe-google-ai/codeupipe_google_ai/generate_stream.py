"""GeminiGenerateStream — streaming text generation via Google Gemini."""


class GeminiGenerateStream:
    """Stream text generation using Google Gemini.

    Reads: ``prompt``, ``api_key`` (or passed at init), ``model``.
    Yields payload chunks with ``chunk_text``.
    """

    def __init__(self, api_key: str = "", model: str = "gemini-pro"):
        self._api_key = api_key
        self._model = model

    async def stream(self, payload):
        import google.generativeai as genai

        genai.configure(api_key=self._api_key or payload.get("api_key"))
        model = genai.GenerativeModel(payload.get("model") or self._model)
        response = model.generate_content(payload.get("prompt"), stream=True)
        for chunk in response:
            if chunk.text:
                yield payload.insert("chunk_text", chunk.text)
