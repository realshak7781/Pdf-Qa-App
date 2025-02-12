from fastapi import FastAPI, File, UploadFile, Depends
import shutil
import os
from pathlib import Path
from database import engine, Base
from pdf_processing import extract_text
from crud import save_pdf_metadata
from models import Document
import uvicorn

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Database initialization
Base.metadata.create_all(bind=engine)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = Path(UPLOAD_DIR) / file.filename
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    text_content = extract_text(str(file_path))
    save_pdf_metadata(file.filename, text_content)

    return {"filename": file.filename, "message": "File uploaded successfully"}

@app.get("/")
async def root():
    return {"message": "PDF Q&A API is running"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
