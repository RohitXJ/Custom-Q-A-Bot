MAX_TOKEN = 250 

def chunker(text: str, doc_id: str,chunk_id):
    print("Chunking\n")
    words = text.split()
    chunks = []
    for i in range(0, len(words), MAX_TOKEN):
        chunk = ' '.join(words[i:i + MAX_TOKEN])
        chunks.append(chunk)
    
    chunk_id_to_text = {f"{doc_id}_chunk_{i}": chunk for i, chunk in enumerate(chunks)}
    chunk_id = chunk_id | chunk_id_to_text
    return chunk_id,chunks
