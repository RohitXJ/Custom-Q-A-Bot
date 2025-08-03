import fitz
import json

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

#print(load_txt("sample_txt.txt"))
#print(load_pdf("sample_pdf.pdf"))
#print(load_json("sample_json.json"))