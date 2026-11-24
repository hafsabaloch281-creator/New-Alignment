import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

MODEL_ID = "Ahm-d18/qwen-base-alignment-lab"
SPACE_URL = "https://ahm-d18-qwen-alignment-lab-app.hf.space"


@app.get("/", response_class=HTMLResponse)
def home():
  return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Lab 10: Qwen Alignment App</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 1100px;
                margin: 30px auto;
                padding: 20px;
                background: #0f172a;
                color: #f8fafc;
            }}
            .card {{
                background: #1e293b;
                padding: 20px;
                border-radius: 10px;
                border: 1px solid #334155;
                margin-bottom: 20px;
            }}
            .btn {{
                display: inline-block;
                padding: 10px 18px;
                background: #3b82f6;
                color: #ffffff;
                text-decoration: none;
                border-radius: 6px;
                font-weight: bold;
                margin-top: 10px;
            }}
            .btn:hover {{
                background: #2563eb;
            }}
            iframe {{
                width: 100%;
                height: 750px;
                border: 1px solid #334155;
                border-radius: 10px;
                background: #0f172a;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Lab 10: Model Alignment Interactive App</h2>
            <p><strong>Model:</strong> <code>{MODEL_ID}</code></p>
            <p><strong>Hugging Face Space:</strong> <code>Ahm-d18/qwen-alignment-lab-app</code></p>
            <a class="btn" href="{SPACE_URL}" target="_blank" rel="noopener noreferrer">Open Full App in New Tab</a>
        </div>
        <iframe src="{SPACE_URL}" title="Qwen Alignment Gradio App"></iframe>
    </body>
    </html>
    """


@app.get("/health")
def health():
  return {
      "status": "ok",
      "model": MODEL_ID,
      "space_url": SPACE_URL,
      "hf_token_configured": bool(os.environ.get("HF_TOKEN")),
  }
