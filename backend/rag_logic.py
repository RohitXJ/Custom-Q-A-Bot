import os
import faiss
from sentence_transformers import SentenceTransformer
from utils.pipeline import run_data_feed_pipeline
from utils.LLM import model_call, build_prompt
from utils.vectorDB import search_faiss
from utils.embedd import query_embedder
import torch

MAX_TOKEN = 100

class RAGSession:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.index_path = os.path.join(data_dir, "index.faiss")
        self.files = {}
        self.current_index = 0

        self.model_embedd = SentenceTransformer('all-MiniLM-L6-v2')
        self.data_id = self.knowledge_base_setup()
        self.LLM_model, self.tokenizer, self.device = model_call()

    def knowledge_base_setup(self):
        for file in os.listdir(self.data_dir):
            if file.endswith(".faiss"):
                continue
            file_path = os.path.join(self.data_dir, file)
            file_format = file.split('.')[-1].lower()
            self.files[file] = [file_path, file_format]

        index = faiss.IndexFlatL2(384)
        faiss.write_index(index, self.index_path)
        del(index)

        chunk_id = run_data_feed_pipeline(self.files, self.model_embedd, self.index_path, self.current_index)
        return chunk_id

    def answer_question(self, question):
        index = faiss.read_index(self.index_path)
        query_vector = query_embedder(question, self.model_embedd)
        top_indices = search_faiss(query_vector, index, top_k=3)
        prompt = build_prompt(question, top_indices, self.data_id)

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        with torch.no_grad():
            outputs = self.LLM_model.generate(
                **inputs,
                max_new_tokens=MAX_TOKEN,
                do_sample=True,
                temperature=0.7,
                top_k=50,
                top_p=0.9,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )

        decoded_output = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer = decoded_output[len(prompt):].strip()

        for stop_token in ["\nQuestion:", "\nQ:", "\n\n"]:
            if stop_token in answer:
                answer = answer.split(stop_token)[0].strip()

        return answer
