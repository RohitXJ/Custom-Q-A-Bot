import os
from utils import I_O_utils as loader

DATA_DIR =  r"DATA_POOL"
files = {}

for file in os.listdir(DATA_DIR):
    file_path = os.path.join(DATA_DIR,file)
    file_format = file.split(".")[1]
    files[file] = [file_path,file_format]

