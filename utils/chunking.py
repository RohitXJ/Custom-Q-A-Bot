from zenml import step
from utils.embedd import embedder
MAX_TOKEN = 250 

@step
def chunker(text):
    print("Chunking\n")
    words = text.split()
    chunks = []
    for i in range(0,len(words),MAX_TOKEN):
        chunk = ' '.join(words[i:i + MAX_TOKEN])
        chunks.append(chunk)
    
    embedder(chunks)