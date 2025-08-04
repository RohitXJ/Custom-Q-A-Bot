from utils.I_O_utils import data_extractor
from utils.embedd import embedder
from utils.chunking import chunker
from utils.vectorDB import add_data_to_VectorDB

def run_data_feed_pipeline(files,embedder_model,index_path):
    chunk_id = {}
    for file in files.keys():
        file_path,file_format = files[file]
        text = data_extractor(file_path,file,file_format)
        chunk_id,chunk = chunker(text,file,chunk_id)
        embeds = embedder(chunk,embedder_model)
        add_data_to_VectorDB(embeds,index_path)

    return chunk_id