from Backend.Agents.Planner_agent import planner_agent


def route_question(question: str) -> dict:
    """
    Router uses Planner Agent result.
    """
    return planner_agent.run(question)