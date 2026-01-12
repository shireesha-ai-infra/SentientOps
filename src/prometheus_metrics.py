from prometheus_client import Counter, Gauge, generate_latest

requests_total = Counter("rag_requests_total", "Total RAG requests")
cache_hits = Counter("rag_cache_hits_total", "Cache hits")
rejections = Counter("rag_rejections_total", "Rejected queries")

latency = Gauge("rag_latency_seconds", "End-to-end latency")
retrieval_time = Gauge("rag_retrieval_time_seconds", "Retrieval latency")
generation_time = Gauge("rag_generation_time_seconds", "Generation latency")
llm_cost = Gauge("rag_llm_cost_usd", "Estimated LLM cost")

def render_metrics():
    return generate_latest()
