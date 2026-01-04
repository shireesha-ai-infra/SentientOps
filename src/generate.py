# Using retreived chunks to answer the question - Augumented Generation
# Mocking the LLM for now
def generate_answer(context_chunks, question):
    context = "\n\n".join(context_chunks)

    prompt = f"""
Use the context below to answer the question.

Context:
{context}

Question:
{question}
"""
    return prompt
