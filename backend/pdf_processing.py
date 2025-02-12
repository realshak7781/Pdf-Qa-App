import fitz  # PyMuPDF
from llama_index import SimpleDirectoryReader, GPTVectorStoreIndex

def extract_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def build_index():
    reader = SimpleDirectoryReader("uploads")
    docs = reader.load_data()
    index = GPTVectorStoreIndex.from_documents(docs)
    return index

def answer_question(index, query: str):
    retriever = index.as_retriever()
    response = retriever.query(query)
    return response.response