from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from pathlib import Path
from database import engine, Base
from pdf_processing import extract_text
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_huggingface import HuggingFaceEndpoint
import dotenv

# Load environment variables
dotenv.load_dotenv()

# Ensure API token is set
HF_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not HF_API_TOKEN:
    raise ValueError("HUGGINGFACEHUB_API_TOKEN not found. Set it in your environment variables.")

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

# Load Hugging Face Model
llm = HuggingFaceEndpoint(
    repo_id="google/flan-t5-large",
    temperature=0.5,
    max_length=512
)

vector_store = None

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

        # Split text into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(text_content)

        # Generate embeddings
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        global vector_store
        vector_store = FAISS.from_texts(texts, embeddings)

        return {"filename": sanitized_filename, "message": "File uploaded and processed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")

@app.post("/ask/")
async def ask_question(question: str):
    try:
        if vector_store is None:
            raise HTTPException(status_code=500, detail="No document processed yet.")

        # Load QA chain
        qa_chain = load_qa_chain(llm, chain_type="stuff")
        docs = vector_store.similarity_search(question, k=5)
        response = qa_chain.run(input_documents=docs, question=question)

        return {"answer": response}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing question: {str(e)}")

@app.get("/")
async def root():
    return {"message": "PDF Q&A API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
