# Using retreived chunks to answer the question - Augumented Generation

from llama_cpp import Llama
from src.prompts import ACTIVE_PROMPT
from src.runtime import is_ci

_llm = None

#Fake llm just for CI
class FakeLLM:
    def __call__(self, prompt, max_tokens=256, stop=None):
        return {
            "choices": [
                {
                    "text": "This is a CI stub answer"
                }
            ]
        }

def get_llm():
    global _llm

    if _llm is not None:
        return _llm
    
    if is_ci():
        print("Running in CI -> Using FakeLLM")
        _llm = FakeLLM()
        return _llm
    
    print("Running Locally -> loading Phi-2")
    # Load model once
    _llm = Llama(
        model_path="models/phi2/phi-2.Q4_K_M.gguf",
        n_ctx=2048,
        n_threads=6,
        temperature=0,
        verbose=False
    )
    return _llm

def generate_answer(context_chunks, question):
    llm = get_llm()
    context = "\n\n".join(context_chunks)

    prompt = ACTIVE_PROMPT.format(
        context = context,
        question = question
    )
    output = llm(
        prompt,
        max_tokens=256,
        stop=["Question:", "Context:"]
    )
    
    return output["choices"][0]["text"].strip()
