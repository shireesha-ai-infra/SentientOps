from functools import lru_cache

_query_cache = {}

# Cache upto 100 recent queries
@lru_cache(maxsize=100)
def normalize_question(question: str) -> str:
    return question.strip().lower()

def get_cached_answer(question:str):
    key = normalize_question(question)
    print("CACHE LOOKUP: ", key, "HIT" if key in _query_cache else "MISS")
    return _query_cache.get(normalize_question(question))

def set_cached_answer(question:str, answer:str):
    _query_cache[normalize_question(question)] = answer

def clear_cache():
    _query_cache.clear()