from sqlalchemy.orm import Session
from models import Document
from database import SessionLocal

def save_pdf_metadata(filename: str, content: str):
    db = SessionLocal()
    document = Document(filename=filename, content=content)
    db.add(document)
    db.commit()
    db.close()
