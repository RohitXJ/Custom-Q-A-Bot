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

def build_prompt(question, top_indices, chunk_map):
    prompt = "Answer the following question using the context below:\n\n"
    for idx in top_indices:
        idx = int(idx)  # Ensure it's int
        if idx in chunk_map:
            prompt += chunk_map[idx] + "\n"
        else:
            print(f"[WARN] Missing chunk index: {idx}")
    prompt += f"\nQuestion: {question}\nAnswer:"
    return prompt

