import faiss
import numpy as np

def add_data_to_VectorDB(embeddings,index_path):
    index = faiss.read_index(index_path)
    embedding_matrix = np.array(embeddings).astype('float32')
    index.add(embedding_matrix)
    faiss.write_index(index, index_path)

def search_faiss(query_vector, index, top_k=3):
    query_vector = np.array(query_vector).astype('float32').reshape(1, -1)
    distances, indices = index.search(query_vector, top_k)
    return indices[0]