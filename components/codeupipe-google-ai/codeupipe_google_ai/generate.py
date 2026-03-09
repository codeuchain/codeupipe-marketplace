"""GeminiGenerate — text generation via Google Gemini."""


class GeminiGenerate:
    """Generate text using Google Gemini.

    Reads: ``prompt``, ``api_key`` (or passed at init), ``model`` (default: gemini-pro).
    Writes: ``generated_text``.
    """

    def __init__(self, api_key: str = "", model: str = "gemini-pro"):
        self._api_key = api_key
        self._model = model

    def call(self, payload):
        import google.generativeai as genai

        genai.configure(api_key=self._api_key or payload.get("api_key"))
        model = genai.GenerativeModel(payload.get("model") or self._model)
        response = model.generate_content(payload.get("prompt"))
        return payload.insert("generated_text", response.text)
