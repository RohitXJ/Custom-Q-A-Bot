import fitz
import json
from zenml import step
from utils.chunking import chunker
import re

def load_txt(PATH):
    with open(PATH,"r",encoding="utf-8") as F:
        return F.read()
    
def load_pdf(PATH):
    doc = fitz.open(PATH)
    text = "" 
    for page in doc:
        text += page.get_text()
    return text

def load_json(PATH):
    with open(PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    def flatten_json(obj, indent=0):
        text = ""
        if isinstance(obj, dict):
            for k, v in obj.items():
                text += "  " * indent + f"{k}: {flatten_json(v, indent+1)}\n"
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                text += flatten_json(item, indent)
        else:
            text += str(obj)
        return text
    return flatten_json(data)

def clean_text(text):
    # Remove extra newlines and spaces
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()

@step
def data_extractor(file_meta): 
    print("Extractting data from files\n")
    for f in file_meta.items():
        file_path,file_format = file_meta[f]
        if file_format == "pdf":
            text = load_pdf(file_path)
        elif file_format == "txt":
            text = load_txt(file_path)
        else:
            text = load_json(file_path)
        text = clean_text(text)
        chunker(text)

    return text

#print(load_txt("sample_txt.txt"))
#print(load_pdf("sample_pdf.pdf"))
#print(load_json("sample_json.json"))