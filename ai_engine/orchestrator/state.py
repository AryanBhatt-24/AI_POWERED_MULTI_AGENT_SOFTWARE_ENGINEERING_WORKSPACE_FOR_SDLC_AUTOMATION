from typing import TypedDict

class State(TypedDict):
    project_id: str
    user_input: str

    requirements: dict | None
    architecture: dict | None
    test_plan: dict | None
    documentation: dict | None

    current_stage: str | None
    review_decision: str | None
    review_feedback: str | None