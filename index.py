import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

MODEL_ID = "Ahm-d18/qwen-base-alignment-lab"


@app.get("/", response_class=HTMLResponse)
def home():
  return f"""
    <html>
        <head><title>Lab 10: Model Alignment</title></head>
        <body style="font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; background: #0f172a; color: #f8fafc; padding: 20px;">
            <h2>Lab 10: Model Alignment Deployment</h2>
            <p><strong>Hugging Face Model:</strong> {MODEL_ID}</p>
            <p>Weights and tokenizer are published on Hugging Face Hub. Serverless inference on Vercel is not active for this custom repository ID (<code>StopIteration</code>), so full model generation is executed in Google Colab.</p>
        </body>
    </html>
    """


@app.get("/health")
def health():
  return {
      "status": "ok",
      "model": MODEL_ID,
      "hf_token_configured": bool(os.environ.get("HF_TOKEN")),
  }
