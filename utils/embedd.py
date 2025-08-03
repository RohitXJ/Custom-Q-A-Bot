from sentence_transformers import SentenceTransformer
from zenml import step

@step
def embedder(chunks):
    print("Embedding\n")
    model_embedd = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model_embedd.encode(chunks)
    dimension = embeddings[0].shape[0]
    add_data_to_VectorDB(embeddings,dimension)