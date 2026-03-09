"""GeminiEmbed — text embeddings via Google Gemini."""


class GeminiEmbed:
    """Generate text embeddings using Google Gemini.

    Reads: ``text``, ``api_key`` (or passed at init), ``model`` (default: models/embedding-001).
    Writes: ``embedding`` (list of floats).
    """

    def __init__(self, api_key: str = "", model: str = "models/embedding-001"):
        self._api_key = api_key
        self._model = model

    def call(self, payload):
        import google.generativeai as genai

        genai.configure(api_key=self._api_key or payload.get("api_key"))
        result = genai.embed_content(
            model=payload.get("model") or self._model,
            content=payload.get("text"),
        )
        return payload.insert("embedding", result["embedding"])
