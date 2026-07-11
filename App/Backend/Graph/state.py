from typing import TypedDict, List, Optional

#TypedDict → Defines the structure of a dictionary.
#List → Means a list.
#Optional → Means the value can either be that type or None.
#MediAssistState is the blueprint.
#state is the actual dictionary created in memory using that blueprint(present graph.py)

class MediAssistState(TypedDict):
    question: str
    route: Optional[str]

    context: str
    chunks: List[str]
    sources: List[str]

    answer: str
    is_valid: bool
    reason: str   #Stores why the planner selected the route or blocked the question.