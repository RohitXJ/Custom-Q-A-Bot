from utils.I_O_utils import data_extractor
from utils.embedd import embedder
from utils.chunking import chunker
from utils.vectorDB import add_data_to_VectorDB

def run_data_feed_pipeline(files,embedder_model,index_path,current_index):
    chunk_id = {}
    for file in files.keys():
        file_path,file_format = files[file]

        """Extracting text from files"""
        text = data_extractor(file_path,file,file_format)

        """Turning whole data into chunks"""
        chunk_id,chunk,current_index = chunker(text,file,chunk_id,current_index)

        """Turning the chunks into vector embeddings"""
        embeds = embedder(chunk,embedder_model)

        """Adding Embeddings to the VectorDB"""
        add_data_to_VectorDB(embeds,index_path)

    return chunk_id