# Execution Guide: SentientOps

Below is the detailed explanation of how to run the SentientOps RAG system, interact with its API, and monitor its performance. It offers two methods of execution: **Docker (Containerized)** and **Local Python**.

## 1. System Overview

SentientOps is a Retrieval-Augmented Generation (RAG) system designed to debug operational incidents using documentation.

*   **Ingest**: Loads PDFs from `data/pdf_files`.
*   **Embed & Store**: Uses `sentence-transformers` and `faiss` to index content.
*   **Retrieve**: Finds relevant chunks for a user query.
*   **Generate**: Uses a local LLM (`phi-2`) via `llama-cpp-python` to answer.
*   **Observe**: Tracks latency, cache hits, and generation time.

## 2. Prerequisites

**For Docker Mode:**
*   Docker & Docker Compose

**For Local Mode:**
*   Python 3.10+
*   Virtual Environment (recommended)

**Data Setup (Required for both):**
*   **Model**: Ensure `models/phi2/phi-2.Q4_K_M.gguf` exists.
*   **PDFs**: Ensure documents are in `data/pdf_files/`.

## 3. Method A: Docker Execution (Recommended)

This method runs the API, Prometheus, and Grafana in orchestrated containers.

1.  **Build and Start**:
    ```bash
    docker-compose up --build -d
    ```
2.  **Verify**:
    ```bash
    docker-compose ps
    ```
    Ensure `api` (Port 8000), `prometheus` (Port 9090), and `grafana` (Port 3000) are `Up`.

## 4. Method B: Local Python Execution

Use this method for development or if Docker networking is restricted.

1.  **Activate Virtual Environment**:
    ```bash
    source .venv/bin/activate
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the API**:
    ```bash
    uvicorn src.api:app --host 0.0.0.0 --port 8080
    ```
    *(Note: We use port **8080** here to avoid conflicts if Docker is partially running. Adjust as needed.)*

## 5. Execution: Asking Questions

You can query the system using `curl`.

**Sample Query**:
```bash
# If running via Docker (Port 8000)
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{ "question": "Explain Kubernetes in one sentence?" }'

# If running Locally (Port 8080)
curl -X POST "http://localhost:8080/query" \
     -H "Content-Type: application/json" \
     -d '{ "question": "Explain Kubernetes in one sentence?" }'
```

**Expected Response**:
```json
{
  "question": "Explain Kubernetes in one sentence?",
  "answer": "Kubernetes is a container orchestration platform...",
  "latency_seconds": 5.32,
  "retrieval_time_seconds": 0.07,
  "generation_time_seconds": 5.24
}
```

## 6. Monitoring & Observability

### Metrics Endpoint
The API exposes raw metrics at `/metrics`.
```bash
curl http://localhost:8000/metrics
# or http://localhost:8080/metrics
```
Response:
```json
{
  "requests": 1,
  "avg_latency": 5.32,
  "avg_retrieval_time": 0.07,
  "avg_generation_time": 5.24
}
```

### Prometheus & Grafana (Docker Only)
If you ran the system with Docker:
1.  **Prometheus**: [http://localhost:9090](http://localhost:9090)
2.  **Grafana**: [http://localhost:3000](http://localhost:3000)

## 7. Troubleshooting

*   **Port Conflicts**: If port 8000 is busy, modify `docker-compose.yml` or the `uvicorn` command to use a different port.
