from sentence_transformers import SentenceTransformer


def embedder(chunks,model):
    print("Embedding\n")
    embeddings = model.encode(chunks)
    return embeddings

def query_embedder(query,model):
    embeddings = model.encode([query])[0]
    return embeddings