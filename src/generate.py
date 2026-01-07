# Using retreived chunks to answer the question - Augumented Generation

from llama_cpp import Llama

# Load model once
llm = Llama(
    model_path="models/llama-2-7b-chat.Q5_K_M.gguf",
    n_ctx=4096,
    n_threads=8,
    temperature=0
)

def generate_answer(context_chunks, question):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an helpful assistant.
Answer the question using ONLY the context below.
If the answer is not present in the context, say "I don't know

Context:
{context}

Question:
{question}
[/INST]
"""
    output = llm(
        prompt,
        max_tokens=512,
        stop=["</s>"]
    )
    
    return output["choices"][0]["text"].strip()
