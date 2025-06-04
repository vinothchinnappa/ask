import cohere
import fitz  # PyMuPDF
import pandas as pd
from docx import Document

co = cohere.Client("67yUWfJ5jc4EkJSOpB197ZVSU7GGXJbYd7EKicE6")

def extract_text_from_file(path, filename):
    if filename.endswith('.pdf'):
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])
    elif filename.endswith('.docx'):
        return "\n".join([para.text for para in Document(path).paragraphs])
    elif filename.endswith('.xlsx') or filename.endswith('.csv'):
        df = pd.read_excel(path) if filename.endswith('.xlsx') else pd.read_csv(path)
        return df.to_string(index=False)
    else:
        return "Unsupported format"

def ask_cohere(context, question):
    response = co.chat(
        message=question,
        documents=[{"title": "doc", "snippet": context[:2000]}],
        temperature=0.3
    )
    return response.text
