def calculate_average(scores: dict):

    total = (
        scores["relevance"]
        + scores["groundedness"]
        + scores["completeness"]
    )

    return round(total / 3, 2)