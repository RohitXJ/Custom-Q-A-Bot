import os
import faiss
from sentence_transformers import SentenceTransformer
from utils.pipeline import run_data_feed_pipeline

DATA_DIR =  r"DATA_POOL"
files = {}
index_path = r"VECTORIZED_DATA_POOL/index.faiss"

model_embedd = SentenceTransformer('all-MiniLM-L6-v2')

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

