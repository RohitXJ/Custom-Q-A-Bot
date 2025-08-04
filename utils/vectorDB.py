from zenml import step

@step
def add_data_to_VectorDB(embeddings,dimension):
    