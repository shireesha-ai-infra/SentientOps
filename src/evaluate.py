from src.pipeline import build_rag_pipeline, ask
from src.eval_questions import EVAL_QUESTIONS
from src.pipeline import PDF_DIR

def run_evaluation():
    print("Running Evaluation....")

    chunks, store = build_rag_pipeline(PDF_DIR)

    for i, question in enumerate(EVAL_QUESTIONS, 1):
        result = ask(question, chunks, store)
        print(f"Q{i}: {question}")
        print(f"A{i}: {result['answer']}")
        print("-"*50)

if __name__ == "__main__":
    run_evaluation()

