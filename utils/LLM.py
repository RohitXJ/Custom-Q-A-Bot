from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

def model_call():
    model_id = "microsoft/phi-2"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16 if device=="cuda" else torch.float32)
    model.to(device)
    model.eval()
    return model,tokenizer,device

def build_prompt(question, top_indices, chunk_map,data_id):
    prompt = f"Answer the following question using the context below:\n\n"
    for idx in top_indices:
        key = f"{data_id}_chunk_{int(idx)}"
        if key in chunk_map:
            prompt += chunk_map[key] + "\n"
        else:
            print(f"[WARN] Missing chunk: {key}")
    prompt += f"\nQuestion: {question}\nAnswer:"
    return prompt

