@app.get("/generate")
def generate(prompt: str):
  if not HF_TOKEN:
    return {"error": "HF_TOKEN is not set on Vercel."}
  try:
    output = client.text_generation(prompt, max_new_tokens=150)
    return {"prompt": prompt, "response": output}
  except Exception as e:
    return {"error": f"{type(e).__name__}: {repr(e)}"}
