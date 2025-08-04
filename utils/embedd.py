from sentence_transformers import SentenceTransformer


def embedder(chunks,model):
    print("Embedding\n")
    embeddings = model.encode(chunks)
    return embeddings