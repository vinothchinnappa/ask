from fastapi import FastAPI, Form
import base64
import tempfile
from utils import extract_text_from_file, ask_cohere

app = FastAPI()
documents = {}

@app.post("/upload")
async def upload_doc(
    file_name: str = Form(...),
    file_base64: str = Form(...)
):
    # Decode base64 content to bytes
    file_bytes = base64.b64decode(file_base64)

    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    # Extract text from file
    text = extract_text_from_file(tmp_path, file_name)
    documents[file_name] = text
    return {"message": "Uploaded", "doc_id": file_name}
