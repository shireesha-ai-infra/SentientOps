# Using retreived chunks to answer the question - Augumented Generation

from llama_cpp import Llama
from src.prompts import ACTIVE_PROMPT

# Load model once
llm = Llama(
    model_path="models/phi2/phi-2.Q4_K_M.gguf",
    n_ctx=2048,
    n_threads=6,
    temperature=0,
    verbose=False
)

def generate_answer(context_chunks, question):
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
