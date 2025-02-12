from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path
from database import engine, Base
from pdf_processing import extract_text
from crud import save_pdf_metadata

# Initialize FastAPI app
app = FastAPI()

# Configure CORS (important for React frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload directory setup
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Database initialization
Base.metadata.create_all(bind=engine)

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    if not file:
        return {"error": "No file received"}

    # Sanitize filename and save file
    sanitized_filename = file.filename.replace(" ", "_")  # Avoid spaces in filenames
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
        return {"error": f"File upload failed: {str(e)}"}

@app.get("/")
async def root():
    return {"message": "PDF Q&A API is running"}

# Run the application (for local development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
