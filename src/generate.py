# Using retreived chunks to answer the question - Augumented Generation
# Plugging in the real OPENAI LLM

from dotenv import load_dotenv
from openai import OpenAI
import os

# Loading the env variable
load_dotenv()

# Create OPENAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("OPENAI_API_KEY loaded:", os.getenv("OPENAI_API_KEY"))

def generate_answer(context_chunks, question):
    context = "\n\n".join(context_chunks)

    prompt = f"""
You are an helpful assistant.
Answer the question using ONLY the context below.
If the answe is not present in the context, say "I don't know

Context:
{context}

Question:
{question}
"""
    response = client.chat.completions.create(
        model= "gpt-5.2",
        messages = [
            {"role":"user", "content":prompt}
        ],
        temperature=0
    )
    return response.choices[0].message.content
