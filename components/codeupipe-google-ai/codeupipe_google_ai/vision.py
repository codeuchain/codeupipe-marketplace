"""GeminiVision — image/multimodal analysis via Google Gemini."""


class GeminiVision:
    """Analyze images using Google Gemini multimodal.

    Reads: ``image`` (PIL Image or bytes), ``prompt`` (optional), ``api_key``.
    Writes: ``vision_text``.
    """

    def __init__(self, api_key: str = "", model: str = "gemini-pro-vision"):
        self._api_key = api_key
        self._model = model

    def call(self, payload):
        import google.generativeai as genai

        genai.configure(api_key=self._api_key or payload.get("api_key"))
        model = genai.GenerativeModel(payload.get("model") or self._model)
        parts = [payload.get("image")]
        prompt = payload.get("prompt")
        if prompt:
            parts.insert(0, prompt)
        response = model.generate_content(parts)
        return payload.insert("vision_text", response.text)
