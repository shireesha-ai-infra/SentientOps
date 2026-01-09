import time

METRICS = {
    "total_requests": 0,
    "total_latency":0.0,
    "total_retrieval_time": 0.0,
    "total_generation_time":0.0
}

def record_request():
    METRICS["total_requests"] +=1

def record_latency(latency):
    METRICS["total_latency"] += latency

def record_retrieval_time(t):
    METRICS["total_retrieval_time"] += t

def record_generation_time(t):
    METRICS["total_generation_time"] += t

def get_metrics():
    if METRICS["total_requests"] == 0:
        return METRICS
    
    return {
        "requests": METRICS["total_requests"],
        "avg_latency": METRICS["total_latency"]/METRICS["total_requests"],
        "avg_retrieval_time": METRICS["total_retrieval_time"] / METRICS["total_requests"],
        "avg_generation_time": METRICS["total_generation_time"]/ METRICS["total_requests"]
    }