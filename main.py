from fastapi import FastAPI, UploadFile, File, Form
from utils import extract_text_from_file, ask_cohere
import tempfile

app = FastAPI()
documents = {}

@app.post("/upload")
async def upload_doc(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    doc_id = file.filename
    text = extract_text_from_file(tmp_path, file.filename)
    documents[doc_id] = text
    return {"message": "Uploaded", "doc_id": doc_id}

@app.post("/ask")
async def ask_question(doc_id: str = Form(...), question: str = Form(...)):
    if doc_id not in documents:
        return {"error": "Document not found"}
    answer = ask_cohere(documents[doc_id], question)
    return {"answer": answer}
