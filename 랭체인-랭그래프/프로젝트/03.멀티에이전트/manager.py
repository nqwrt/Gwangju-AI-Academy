def manager(state):

    question = state["question"]

    if "번역" in question:
        return "english"

    elif any(op in question for op in ["+", "-", "*", "/"]):
        return "math"

    else:
        return "general"