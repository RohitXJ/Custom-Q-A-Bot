import warnings
import os
warnings.filterwarnings("ignore")  # Ignore ALL warnings
from functools import partial
import builtins
import sys
sys.stderr = open(os.devnull, "w")  # Suppress error/warning printing to stderr
try:
    import tqdm
    tqdm.tqdm = partial(tqdm.tqdm, disable=True)
except ImportError:
    pass

import shutil
import uuid
import faiss
import torch
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi import Request

from sentence_transformers import SentenceTransformer
from utils.pipeline import run_data_feed_pipeline
from utils.LLM import model_call, build_prompt
from utils.vectorDB import search_faiss
from utils.embedd import query_embedder

# ===== CONFIG =====
MAX_TOKEN = 100
DATA_DIR = "DATA_POOL"
INDEX_DIR = "VECTORIZED_DATA_POOL"
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(INDEX_DIR, exist_ok=True)

# ===== FASTAPI APP =====
app = FastAPI()

# Enable CORS (for frontend JS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static and Templates
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
app.mount("/images", StaticFiles(directory="frontend/images"), name="images")
templates = Jinja2Templates(directory="frontend/templates")

# ===== MODEL SETUP =====
model_embedd = SentenceTransformer('all-MiniLM-L6-v2')
LLM_model, tokenizer, device = model_call()

# ===== SESSION MEMORY =====
sessions = {}

# ===== ROUTES =====
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_files(files: list[UploadFile] = File(...)):
    session_id = str(uuid.uuid4())
    user_data_dir = os.path.join(DATA_DIR, session_id)
    os.makedirs(user_data_dir, exist_ok=True)

    # Add preset file
    preset_file_path = "DATA_POOL/sample_txt.txt"
    shutil.copy(preset_file_path, user_data_dir)

    file_map = {}
    # Add preset file to file_map
    file_map["sample_txt.txt"] = [os.path.join(user_data_dir, "sample_txt.txt"), "txt"]

    for file in files:
        file_path = os.path.join(user_data_dir, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        file_map[file.filename] = [file_path, file.filename.split('.')[-1].lower()]

    index_path = os.path.join(INDEX_DIR, f"{session_id}.faiss")
    index = faiss.IndexFlatL2(384)
    faiss.write_index(index, index_path)

    data_id = run_data_feed_pipeline(file_map, model_embedd, index_path, 0)

    sessions[session_id] = {
        "data_dir": user_data_dir,
        "data_id": data_id,
        "index_path": index_path
    }

    return {"session_id": session_id, "message": "Files uploaded & indexed successfully."}

@app.post("/chat")
async def chat(session_id: str = Form(...), question: str = Form(...)):
    if session_id not in sessions:
        return JSONResponse(status_code=404, content={"error": "Invalid session ID"})

    session_data = sessions[session_id]
    index = faiss.read_index(session_data["index_path"])
    query_vector = query_embedder(question, model_embedd)
    top_indices = search_faiss(query_vector, index, top_k=3)

    data_id = session_data["data_id"]
    prompt = build_prompt(question, top_indices, data_id)

    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = LLM_model.generate(
            **inputs,
            max_new_tokens=MAX_TOKEN,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = decoded_output[len(prompt):].strip()

    for stop_token in ["\nQuestion:", "\nQ:", "\n\n"]:
        if stop_token in answer:
            answer = answer.split(stop_token)[0].strip()

    return {"answer": answer}

@app.post("/end-session")
async def end_session(session_id: str = Form(...)):
    if session_id in sessions:
        session_data = sessions.pop(session_id)
        shutil.rmtree(session_data["data_dir"], ignore_errors=True)
        if os.path.exists(session_data["index_path"]):
            os.remove(session_data["index_path"])
    return {"message": "Session ended and files deleted."}
