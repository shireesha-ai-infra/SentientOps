from src.pipeline import build_rag_pipeline, ask, PDF_DIR

def run_smoke_test():
    chunks, store = build_rag_pipeline(PDF_DIR)
    result = ask("What is attention mechanism?", chunks, store)

    assert result["answer"] is not None
    assert len(result["answer"])>10

if __name__ == "__main__":
    run_smoke_test()
