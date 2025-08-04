import os
import faiss
from sentence_transformers import SentenceTransformer
from utils.pipeline import run_data_feed_pipeline
from utils.LLM import model_call,build_prompt
from utils.vectorDB import search_faiss
from utils.embedd import query_embedder
import torch

MAX_TOKEN = 250 
DATA_DIR =  r"DATA_POOL"
files = {}
index_path = r"VECTORIZED_DATA_POOL/index.faiss"

model_embedd = SentenceTransformer('all-MiniLM-L6-v2')
def knowledge_base_setup():
    for file in os.listdir(DATA_DIR):
        file_path = os.path.join(DATA_DIR,file)
        file_format = file.split('.')[-1].lower()
        files[file] = [file_path,file_format]

    print(files)
    index = faiss.IndexFlatL2(384)
    faiss.write_index(index,index_path)
    del(index)

    chunk_id = run_data_feed_pipeline(files,model_embedd,index_path)
    print(chunk_id.keys())
    return chunk_id

def LLM_call():
    data_id = knowledge_base_setup()
    LLM_model,tokenizer,device =  model_call()
    while True:
        question = input(" <- ")
        if question.lower() in ['exit','bye']:
            break
        index = faiss.read_index(index_path)
        query_vector = query_embedder(question, model_embedd)
        top_indices = search_faiss(query_vector, index, top_k=3)
        prompt = build_prompt(question, top_indices, data_id, data_id)


        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        with torch.no_grad():
            outputs = LLM_model.generate(
                **inputs,
                max_new_tokens=MAX_TOKEN,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.9
            )
        answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(answer.strip())

if __name__ == "__main__":
    LLM_call()