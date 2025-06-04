import os
import cohere
import fitz  # PyMuPDF
import pandas as pd
from docx import Document

# Load from environment variable
api_key = os.environ.get("COHERE_API_KEY")
if not api_key:
    raise ValueError("Missing COHERE_API_KEY environment variable")

co = cohere.Client(api_key)

def extract_text_from_file(path, filename):
    filename = filename.lower()
    
    if filename.endswith('.pdf'):
        doc = fitz.open(path)
        return "\n".join([page.get_text() for page in doc])
    
    elif filename.endswith('.docx'):
        return "\n".join([para.text for para in Document(path).paragraphs])
    
    elif filename.endswith('.xlsx'):
        df = pd.read_excel(path)
        return df.to_string(index=False)
    
    elif filename.endswith('.csv'):
        df = pd.read_csv(path)
        return df.to_string(index=False)
    
    else:
        return "Unsupported file format."

def ask_cohere(context, question):
    response = co.chat(
        message=question,
        documents=[{"title": "Document", "snippet": context[:2000]}],
        temperature=0.3
    )
    return response.text
