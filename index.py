import os
from fastapi import FastAPI
from huggingface_hub import InferenceClient

app = FastAPI()

MODEL_ID = "Ahm-d18/qwen-base-alignment-lab"
HF_TOKEN = os.environ.get("HF_TOKEN")

client = InferenceClient(model=MODEL_ID, token=HF_TOKEN)


@app.get("/")
def root():
  return {"status": "ok", "model": MODEL_ID}


@app.get("/generate")
def generate(prompt: str):
  output = client.text_generation(prompt, max_new_tokens=150)
  return {"prompt": prompt, "response": output}
