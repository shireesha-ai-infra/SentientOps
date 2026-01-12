import time

METRICS = {
    "total_requests": 0,
    "total_latency":0.0,
    "total_retrieval_time": 0.0,
    "total_generation_time":0.0,
    "cache_hits":0,
    "rejected_queries":0,
    "avg_latency": 0.0,
    "avg_retrieval_time": 0.0,
    "avg_generation_time": 0.0,
    "total_tokens":0,
    "estimated_cost_usd":0.0

}

COST_PER_1K_TOKENS = 0.002 

def record_request():
    METRICS["total_requests"] +=1

def record_latency(latency):
    METRICS["total_latency"] += latency

def record_retrieval_time(t):
    METRICS["total_retrieval_time"] += t

def record_generation_time(t):
    METRICS["total_generation_time"] += t

def record_cache_hit():
    METRICS["cache_hits"] += 1

def record_rejection():
    METRICS["rejected_queries"] += 1

def record_tokens(n_tokens):
    METRICS["total_tokens"] += n_tokens
    METRICS["estimated_cost_usd"] = (
        METRICS["total_tokens"]/1000 * COST_PER_1K_TOKENS
    )

def record_avg_latency(latency):
    n = METRICS["total_requests"]
    METRICS["avg_latency"] = ((METRICS["avg_latency"] * (n - 1)) + latency) / n

def record_avg_retrieval_time(t):
    n = METRICS["total_requests"]
    METRICS["avg_retrieval_time"] = ((METRICS["avg_retrieval_time"] * (n - 1)) + t) / n

def record_avg_generation_time(t):
    n = METRICS["total_requests"]
    METRICS["avg_generation_time"] = ((METRICS["avg_generation_time"] * (n - 1)) + t) / n


def get_metrics():
    if METRICS["total_requests"] == 0:
        return METRICS
    
    return {
        "requests": METRICS["total_requests"],
        "avg_latency": METRICS["total_latency"]/METRICS["total_requests"],
        "avg_retrieval_time": METRICS["total_retrieval_time"] / METRICS["total_requests"],
        "avg_generation_time": METRICS["total_generation_time"]/ METRICS["total_requests"]
    }