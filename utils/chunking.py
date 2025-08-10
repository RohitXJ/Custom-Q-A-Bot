MAX_TOKEN = 250 

def chunker(text: str, doc_id: str,chunk_id,current_index):
    words = text.split()
    chunks = []
    for i in range(0, len(words), MAX_TOKEN):
        chunk = ' '.join(words[i:i + MAX_TOKEN])
        chunks.append(chunk)
    
    for chunk in chunks:
        chunk_id[current_index]=chunk
        current_index += 1
    return chunk_id,chunks,current_index
