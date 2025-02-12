import fitz  # PyMuPDF
from llama_index.core import SimpleDirectoryReader  # Updated import path
from llama_index.core import VectorStoreIndex  # Updated import path

def extract_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def build_index():
    reader = SimpleDirectoryReader("uploads")
    docs = reader.load_data()
    index = VectorStoreIndex.from_documents(docs)  # Updated class name
    return index

def answer_question(index, query: str):
    query_engine = index.as_query_engine()  # Updated method
    response = query_engine.query(query)
    return response.response