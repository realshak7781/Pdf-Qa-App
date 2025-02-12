from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path
from database import engine, Base
from pdf_processing import extract_text
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS  # Updated import
from huggingface_hub import InferenceClient
import dotenv
from pydantic import BaseModel

# Load environment variables
dotenv.load_dotenv()

# Ensure API token is set
HF_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HF_API_TOKEN:
    raise ValueError("⚠️ HUGGINGFACEHUB_API_TOKEN not found. Set it in your .env file!")

# Initialize FastAPI app
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

# Hugging Face Model Client
client = InferenceClient(model="google/flan-t5-large", token=HF_API_TOKEN)

# Global variable for vector store
vector_store = None

# Pydantic Model for `/ask/` endpoint
class QuestionRequest(BaseModel):
    question: str

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """Uploads and processes a PDF file for question answering."""
    if not file:
        raise HTTPException(status_code=400, detail="No file received")

    sanitized_filename = file.filename.replace(" ", "_")  # Avoid spaces
    file_path = Path(UPLOAD_DIR) / sanitized_filename

    try:
        # Save the uploaded file
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Extract text from PDF
        text_content = extract_text(str(file_path))

        if not text_content:
            raise HTTPException(status_code=400, detail="No text found in the PDF")

        # Split text into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(text_content)

        # Generate embeddings and create vector store
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        global vector_store
        vector_store = FAISS.from_texts(texts, embeddings)

        return {"filename": sanitized_filename, "message": "✅ File uploaded and processed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ File upload failed: {str(e)}")

@app.post("/ask/")
async def ask_question(request: QuestionRequest):
    """Processes a user question and returns an answer."""
    try:
        if vector_store is None:
            raise HTTPException(status_code=400, detail="⚠️ No document processed yet. Upload a PDF first.")

        # Retrieve relevant document chunks
        docs = vector_store.similarity_search(request.question, k=5)
        context = "\n".join([doc.page_content for doc in docs])

        # Debugging: Print context and question
        print(f"Context: {context}")
        print(f"Question: {request.question}")

        # Prepare query for Hugging Face model
        prompt = f"Context: {context}\n\nQuestion: {request.question}\n\nAnswer:"
        
        # Generate response with valid max_new_tokens
        response = client.text_generation(
            prompt,
            max_new_tokens=250,  # Reduced to 250 to comply with model limits
            temperature=0.5
        )

        return {"answer": response}

    except Exception as e:
        print(f"❌ Error in ask_question: {str(e)}")  # Debugging: Print the error
        raise HTTPException(status_code=500, detail=f"❌ Error processing question: {str(e)}")

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "✅ PDF Q&A API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)