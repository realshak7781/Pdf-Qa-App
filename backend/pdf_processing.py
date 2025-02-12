import fitz  # PyMuPDF
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings  # Updated import
from langchain_community.vectorstores import FAISS  # Updated import
from langchain.chains.question_answering import load_qa_chain
from langchain_community.llms import HuggingFaceHub  # Updated import

def extract_text(pdf_path: str) -> str:
    """Extracts text from a PDF file."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        print(f"🚨 Error in extract_text: {str(e)}")
        return ""

def build_index(pdf_path: str):
    """Extracts text, creates embeddings, and stores them in FAISS."""
    try:
        print("📂 Extracting text from PDF...")
        text = extract_text(pdf_path)
        
        if not text:
            raise ValueError("❌ No text found in the provided PDF.")

        print("✅ Text extracted successfully! Splitting into chunks...")
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_text(text)

        print(f"✅ Split into {len(texts)} chunks. Generating embeddings...")
        embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vector_store = FAISS.from_texts(texts, embed_model)

        print("✅ Index built successfully!")
        return vector_store
    
    except Exception as e:
        print(f"🚨 Error in build_index: {str(e)}")
        return None

def answer_question(vector_store, query: str):
    """Answers a query using the indexed documents."""
    try:
        if vector_store is None:
            raise ValueError("❌ Vector store is None. Cannot process query.")
        
        print("🔍 Loading LLM from Hugging Face Hub...")
        # Ensure the API token is set
        if "HUGGINGFACEHUB_API_TOKEN" not in os.environ:
            raise ValueError("❌ Hugging Face API token not found in environment variables.")
        
        llm = HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature": 0.7, "max_length": 512})
        
        qa_chain = load_qa_chain(llm, chain_type="stuff")
        docs = vector_store.similarity_search(query, k=3)
        response = qa_chain.run(input_documents=docs, question=query)
        
        return response
    
    except Exception as e:
        print(f"🚨 Error in answer_question: {str(e)}")
        return "An error occurred while processing the question."

# Example usage
if __name__ == "__main__":
    pdf_path = "path/to/your/pdf.pdf"
    vector_store = build_index(pdf_path)
    
    if vector_store:
        query = "What is the main topic of the document?"
        answer = answer_question(vector_store, query)
        print(f"🤖 Answer: {answer}")