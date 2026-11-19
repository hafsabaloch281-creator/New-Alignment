import os
import traceback
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from huggingface_hub import InferenceClient

app = FastAPI()

MODEL_ID = "Ahm-d18/qwen-base-alignment-lab"
HF_TOKEN = os.environ.get("HF_TOKEN")
client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)


@app.get("/", response_class=HTMLResponse)
def home():
  return f"""
    <html>
        <head>
            <title>Lab 10: LLM Alignment</title>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; background: #0f172a; color: #f8fafc; }}
                textarea {{ width: 100%; height: 100px; padding: 10px; border-radius: 6px; border: 1px solid #334155; background: #1e293b; color: white; }}
                button {{ margin-top: 10px; padding: 10px 20px; background: #3b82f6; color: white; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; }}
                button:hover {{ background: #2563eb; }}
                #output {{ margin-top: 20px; padding: 15px; background: #1e293b; border-radius: 6px; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <h2>Lab 10: Model Inference</h2>
            <p><strong>Model:</strong> {MODEL_ID}</p>
            <textarea id="prompt" placeholder="Enter your prompt here...">Explain what In-Contextual Learning is.</textarea>
            <br>
            <button onclick="generate()">Generate Response</button>
            <div id="output">Response will appear here...</div>

            <script>
                async function generate() {{
                    const prompt = document.getElementById('prompt').value;
                    const out = document.getElementById('output');
                    out.innerText = "Generating...";
                    try {{
                        const res = await fetch('/generate?prompt=' + encodeURIComponent(prompt));
                        const data = await res.json();
                        out.innerText = data.response || JSON.stringify(data);
                    }} catch (err) {{
                        out.innerText = "Error: " + err;
                    }}
                }}
            </script>
        </body>
    </html>
    """


@app.get("/generate")
def generate(prompt: str):
  if not HF_TOKEN:
    return {"error": "HF_TOKEN is missing in this Vercel environment."}
  try:
    output = client.text_generation(prompt, max_new_tokens=150)
    return {"prompt": prompt, "response": output}
  except Exception as e:
    traceback.print_exc()
    return {"error": f"{type(e).__name__}: {repr(e)}"}
