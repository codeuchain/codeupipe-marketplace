# codeupipe-google-ai

Google AI (Gemini) — multimodal generation, embeddings, and vision for codeupipe pipelines.

## Install

```bash
cup marketplace install codeupipe-google-ai
```

## Filters

| Filter | Description |
|--------|-------------|
| `GeminiGenerate` | Text generation via Gemini |
| `GeminiGenerateStream` | Streaming text generation |
| `GeminiEmbed` | Text embeddings |
| `GeminiVision` | Image/multimodal analysis |

## Usage

```python
from codeupipe import Payload, Pipeline
from codeupipe_google_ai import GeminiGenerate

pipeline = Pipeline()
pipeline.add_filter(GeminiGenerate(api_key="..."), name="generate")

result = await pipeline.run(Payload({"prompt": "Explain pipelines in one sentence."}))
print(result.get("generated_text"))
```
