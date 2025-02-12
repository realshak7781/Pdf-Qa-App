from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path
from database import engine, Base
from pdf_processing import extract_text, build_index, answer_question
from crud import save_pdf_metadata
from pydantic import BaseModel

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file received"}

    sanitized_filename = file.filename.replace(" ", "_")  # Avoid spaces
    file_path = Path(UPLOAD_DIR) / sanitized_filename

    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from PDF
        text_content = extract_text(str(file_path))

        # Save metadata
        save_pdf_metadata(sanitized_filename, text_content)

        return {"filename": sanitized_filename, "message": "File uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask/")
async def ask_question(request: QuestionRequest):
    try:
        print(f"🧐 Received question: {request.question}")

        index = build_index()
        if index is None:
            raise HTTPException(status_code=500, detail="Index could not be built.")

        response = answer_question(index, request.question)

        return {"answer": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/")
async def root():
    return {"message": "PDF Q&A API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
