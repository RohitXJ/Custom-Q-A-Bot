from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import sqlite3
import shutil

app = FastAPI()

# Mount static files for frontend
app.mount("/static", StaticFiles(directory="../static"), name="static")

# --- Database setup ---
DB_PATH = "chunks.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT
)
''')
conn.commit()
conn.close()


@app.get("/")
async def root():
    return JSONResponse({"message": "Backend is running"})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Save file temporarily
        temp_path = f"temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Read and split into chunks
        with open(temp_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()

        chunks = [text[i:i+500] for i in range(0, len(text), 500)]

        # Store chunks in SQLite
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("DELETE FROM chunks")  # Clear old chunks
        for ch in chunks:
            c.execute("INSERT INTO chunks (content) VALUES (?)", (ch,))
        conn.commit()
        conn.close()

        os.remove(temp_path)

        return JSONResponse({"message": f"File uploaded successfully, {len(chunks)} chunks stored."})
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/query")
async def query_file(question: str = Form(...)):
    try:
        # Fetch chunks from DB
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT content FROM chunks")
        data = c.fetchall()
        conn.close()

        if not data:
            return JSONResponse({"answer": "No data available. Please upload a file first."})

        # Simple mock answer (replace with LLM later)
        context = " ".join([row[0] for row in data])
        answer = f"Q: {question}\n\nContext snippet: {context[:200]}..."
        
        return JSONResponse({"answer": answer})
    
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
