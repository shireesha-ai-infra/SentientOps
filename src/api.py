from fastapi import FastAPI
from pydantic import BaseModel

from src.pipeline import build_rag_pipeline, ask

app = FastAPI()

PDF_DIR = "data/pdf_files"
chunks, store = build_rag_pipeline(PDF_DIR)

# -------- REQUEST SCHEMA --------------
class QueryRequest(BaseModel):
    question: str

# --------- API Endpoint -----------------
@app.post("/query")
def query_rag(request: QueryRequest):
    answer = ask(request.question, chunks, store)
    return {
        "question" : request.question,
        "answer" : answer
    }

# ----------- Health check ----------------
@app.get("/health")
def health():
    return {"status": "ok"}