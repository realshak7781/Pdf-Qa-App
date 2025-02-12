import fitz  # PyMuPDF
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def extract_text(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def build_index():
    """Builds an index from PDFs in the 'uploads' directory using local embeddings."""
    try:
        print("📂 Loading PDFs from 'uploads' directory...")
        reader = SimpleDirectoryReader("uploads")
        docs = reader.load_data()
        
        if not docs:
            raise ValueError("❌ No PDF documents found in 'uploads' directory.")

        print(f"✅ Loaded {len(docs)} documents. Building index...")

        # Use HuggingFace Embeddings (Local Model)
        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

        index = VectorStoreIndex.from_documents(docs, embed_model=embed_model)

        print("✅ Index built successfully!")
        return index

    except Exception as e:
        print(f"🚨 Error in build_index: {str(e)}")
        return None

def answer_question(index, query: str):
    """Answers a query using the indexed documents."""
    try:
        if index is None:
            raise ValueError("❌ Index is None. Cannot process query.")

        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        return response.response

    except Exception as e:
        print(f"🚨 Error in answer_question: {str(e)}")
        return "An error occurred while processing the question."
