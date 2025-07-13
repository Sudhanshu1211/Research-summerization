import os
from typing import Tuple
from src.utils.session_store import session_store
from src.components.summarizer import generate_summary
from src.utils.file_utils import read_txt_file, read_pdf_file

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'uploads')

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_and_parse_document(file, filename: str) -> Tuple[str, str]:
    """
    Save uploaded file, parse text, create session, and generate summary.
    Returns (session_id, summary)
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    with open(file_path, 'wb') as f:
        f.write(file)
    
    if filename.lower().endswith('.pdf'):
        text = read_pdf_file(file_path)
    elif filename.lower().endswith('.txt'):
        text = read_txt_file(file_path)
    else:
        raise ValueError('Unsupported file type')

    summary = generate_summary(text)
    session_id = session_store.create_session({'filename': filename, 'file_path': file_path, 'text': text, 'summary': summary})
    return session_id, summary

def get_document_text(session_id: str) -> str:
    session = session_store.get_session(session_id)
    return session.get('text', '')

def get_summary(session_id: str) -> str:
    session = session_store.get_session(session_id)
    return session.get('summary', '')
