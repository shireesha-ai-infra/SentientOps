# Using retreived chunks to answer the question - Augumented Generation

from llama_cpp import Llama

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

    prompt = f"""Instruction:
You are an helpful assistant.

Use ONLY the information in the context below to answer the question.
If the answer cannot be found in the context, respond exactly with "I don't know

Context:
{context}

Question:
{question}

Answer:
"""
    output = llm(
        prompt,
        max_tokens=256,
        stop=["Question:", "Context:"]
    )
    
    return output["choices"][0]["text"].strip()
