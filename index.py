import gradio as gr
import spaces
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL_ID = "Ahm-d18/qwen-base-alignment-lab"

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID, torch_dtype=torch.float16, low_cpu_mem_usage=True
)
model.eval()


@spaces.GPU(duration=60)
def predict(prompt: str, max_new_tokens: int = 128) -> str:
  if not prompt or not prompt.strip():
    return "Please enter a prompt."

  device = "cuda" if torch.cuda.is_available() else "cpu"
  model.to(device)

  if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
    text = tokenizer.apply_chat_template(
        [{"role": "user", "content": prompt.strip()}],
        tokenize=False,
        add_generation_prompt=True,
    )
  else:
    text = prompt.strip()

  inputs = tokenizer(text, return_tensors="pt").to(device)
  with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=int(max_new_tokens),
        do_sample=False,
        pad_token_id=tokenizer.eos_token_id,
    )
  gen_ids = outputs[0][inputs["input_ids"].shape[1] :]
  return tokenizer.decode(gen_ids, skip_special_tokens=True).strip()


demo = gr.Interface(
    fn=predict,
    inputs=[
        gr.Textbox(
            lines=3,
            label="Prompt",
            value="Explain what In-Contextual Learning.",
        ),
        gr.Slider(32, 256, value=128, step=16, label="Max New Tokens"),
    ],
    outputs=gr.Textbox(lines=10, label="Model Prediction"),
    title="Lab 10: Qwen Alignment Model App",
    description=f"Model: `{MODEL_ID}`",
)

if __name__ == "__main__":
  demo.launch()
