from fastapi import FastAPI
from pydantic import BaseModel

from src.metrics import get_metrics
from src.pipeline import build_rag_pipeline, ask
from src.prometheus_metrics import render_metrics
from fastapi.responses import PlainTextResponse

app = FastAPI()

PDF_DIR = "data/pdf_files"

chunks, store = build_rag_pipeline(PDF_DIR)

# -------- REQUEST SCHEMA --------------
class QueryRequest(BaseModel):
    question: str

# --------- API Endpoint -----------------
@app.post("/query")
def query_rag(request: QueryRequest):

    result = ask(request.question, chunks, store)

    return {
        "question" : request.question,
        "answer" : result["answer"],
        "latency_seconds": result["latency_seconds"],
        "retrieval_time_seconds": result["retrieval_time_seconds"],
        "generation_time_seconds": result["generation_time_seconds"]
    }

# ----------- Metrics ---------------------
@app.get("/metrics")
def metrics():
    return get_metrics()

# ----------- Health check ----------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metrics_prom", response_class=PlainTextResponse)
def prometheus_metrics():
    return render_metrics()
