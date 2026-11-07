from orchestrator.state import State
from orchestrator.workflow import workflow
from langgraph.types import Command

initial_state: State = {
    "project_id": "project_001",

    "user_input": """
    Build an AI-powered task management application.
    Users should be able to register, log in, create tasks,
    set deadlines, track progress and receive notifications.
    """,

    "requirements": None,
    "architecture": None,
    "test_plan": None,
    "documentation": None,
    "current_stage": None,
    "review_decision": None,
    "review_feedback": None
}

config = {
    "configurable": {
        "thread_id": "project_001"
    }
}

result = workflow.invoke(initial_state, config=config)

while "__interrupt__" in result:
    interrupt_info = result["__interrupt__"][0].value

    print("\n========== HUMAN REVIEW ==========")
    print("Stage:", interrupt_info["stage"])
    print("Output:", interrupt_info["output"])

    decision = input("\nEnter approve/revise: ").strip().lower()

    while decision not in ["approve", "revise"]:
        decision = input("Please enter approve or revise: ").strip().lower()

    feedback = ""

    if decision == "revise":
        feedback = input("Enter your feedback: ").strip()

    result = workflow.invoke(
        Command(
            resume={
                "decision": decision,
                "feedback": feedback
            }
        ),
        config=config
    )
