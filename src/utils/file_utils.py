def read_txt_file(file_path: str) -> str:
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def read_pdf_file(file_path: str) -> str:
    try:
        from PyPDF2 import PdfReader
    except ImportError:
        raise ImportError('PyPDF2 is required for PDF parsing')
    reader = PdfReader(file_path)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''
    return text
