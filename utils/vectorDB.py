import faiss
import numpy as np

def add_data_to_VectorDB(embeddings,index_path):
    index = faiss.read_index(index_path)
    embedding_matrix = np.array(embeddings).astype('float32')
    index.add(embedding_matrix)
    faiss.write_index(index, index_path)