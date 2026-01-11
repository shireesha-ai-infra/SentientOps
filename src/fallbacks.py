def no_context_fallback(question: str):
    return (
        "I don’t have enough information in my documents "
        "to answer that question confidently."
    )

def generation_error_fallback():
    return (
        "I’m having trouble generating an answer right now. "
        "Please try again in a moment."
    )

def system_error_fallback():
    return (
        "Something went wrong on our side. "
        "The issue has been logged."
    )