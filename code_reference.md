# SentientOps Codebase Documentation

This document provides a detailed reference for the SentientOps codebase, explaining the purpose of each file, function, and key variable.

## Source Directory (`src/`)

### `src/api.py`
**Purpose**: The entry point for the FastAPI application. It defines the API endpoints and integrates the RAG pipeline.

*   **`app`** (`FastAPI`): The main application instance.
*   **`QueryRequest`** (`BaseModel`): Pydantic model defining the request body for `/query` (expects a `question` string).
*   **`query_rag(request: QueryRequest)`**: POST `/query`. Receives a user question, processes it through `ask()`, and returns the answer with metrics.
*   **`metrics()`**: GET `/metrics`. Returns internal application metrics (JSON format).
*   **`health()`**: GET `/health`. Simple health check returning `{"status": "ok"}`.
*   **`prometheus_metrics()`**: GET `/metrics_prom`. Exposes metrics in OpenMetrics format for Prometheus scraping.

### `src/pipeline.py`
**Purpose**: Orchestrates the RAG flow (Retrieve, Augmented Generate). Connects ingestion, embedding, searching, and generation.

*   **Constants**:
    *   `VECTOR_STORE_PATH`, `CHUNKS_PATH`, `PDF_DIR`: Paths for data storage.
*   **`build_rag_pipeline(pdf_dir)`**: Initializes the system. Loads the vector store from disk if it exists; otherwise, triggers ingestion (`load_pdfs`) and embedding (`create_embeddings`) to build a new index.
*   **`ask(question, chunks, store)`**: The core logic function.
    1.  Checks cache.
    2.  Embeds the query.
    3.  Searches the vector store.
    4.  Applies the **Grounding Gate** (checks similarity threshold).
    5.  Calls the LLM (`generate_answer`) if grounded.
    6.  Records detailed metrics (latency, retrieval time, etc.).
    7.  Updates cache and returns the result.

### `src/ingest.py`
**Purpose**: Handles loading of raw data (PDFs).

*   **`load_pdfs(pdf_dir)`**: Scans the specified directory for `.pdf` files, reads them using `pypdf`, and returns a list of extracted text strings.

### `src/embed.py`
**Purpose**: Manages text-to-vector embeddings.

*   **`model`** (`SentenceTransformer`): The loaded embedding model (`all-MiniLM-L6-v2`).
*   **`create_embeddings(texts, chunk_size)`**: Splits raw texts into chunk of `chunk_size` (default 500 characters) and converts them into vector embeddings. Returns both the text chunks and their corresponding vector array.

### `src/retrieve.py`
**Purpose**: Wraps the vector database/search engine.

*   **`VectorStore`** (`class`): Wrapper around `faiss`.
    *   **`__init__(embeddings)`**: initializes a FlatL2 FAISS index and adds the provided embeddings.
    *   **`search(query_embedding, top_k)`**: Searches the index for the `top_k` (default 3) nearest neighbors. Returns indices and similarity scores (converted from L2 distance).

### `src/generate.py`
**Purpose**: Interfaces with the Large Language Model (LLM).

*   **`get_llm()`**: Singleton pattern to load the `phi-2` model via `llama_cpp` (or a `FakeLLM` if in CI environment).
*   **`generate_answer(context_chunks, question)`**: Constructs the prompt using `ACTIVE_PROMPT`, invokes the LLM, and allows for a timeout (handled in pipeline).

### `src/cache.py`
**Purpose**: Simple in-memory caching mechanism.

*   **`normalize_question(question)`**: Trims and lowercases the question for consistent keying.
*   **`get_cached_answer(question)`**: Looks up a normalized question in the `_query_cache`.
*   **`set_cached_answer(question, answer)`**: Stores the answer mapped to the normalized question.
*   **`clear_cache()`**: Empties the cache.

### `src/metrics.py`
**Purpose**: Custom internal metrics tracking dictionary.

*   **`METRICS`** (`dict`): Stores counters and rolling averages (e.g., `requests_total`, `avg_latency`).
*   **`record_request()`, `record_latency(val)`, etc.**: Helper functions to update specific keys in the `METRICS` dictionary.
*   **`get_metrics()`**: Returns a clean view of the current metrics state.

### `src/prometheus_metrics.py`
**Purpose**: Defines Prometheus collectors.

*   **Variables** (`Counter`, `Gauge`):
    *   `requests_total`, `cache_hits`, `rejections`
    *   `latency`, `retrieval_time`, `generation_time`, `llm_cost`
*   **`render_metrics()`**: Exports these metrics as a string compatible with Prometheus scraping.

### `src/logging_utils.py`
**Purpose**: centralized logging.

*   **`logger`**: Configured to write to `rag_system.log` and stdout.
*   **`log_query()`, `log_latency()`, etc.**: Structured helpers to ensure consistent log formats.

### `src/timeouts.py`
**Purpose**: Utility for limiting function execution time.

*   **`run_with_timeout(func, timeout_seconds)`**: Runs a function in a thread pool and raises `TimeoutException` if it exceeds the limit.

### `src/fallbacks.py`
**Purpose**: Standardized error messages.

*   **`no_context_fallback()`**: "I don’t have enough information..."
*   **`generation_error_fallback()`**: "I’m having trouble generating..."
*   **`system_error_fallback()`**: "Something went wrong..."

### `src/prompts.py`
**Purpose**: Storage for LLM prompts.

*   **`PROMPT_V1`**: The default RAG prompt template injected with `{context}` and `{question}`.

### `src/reindex.py`
**Purpose**: Utility script to manually force a re-index.

*   **`rebuild_index()`**: Clears existing data, re-runs ingestion and embedding, and saves the new artifacts to disk.
