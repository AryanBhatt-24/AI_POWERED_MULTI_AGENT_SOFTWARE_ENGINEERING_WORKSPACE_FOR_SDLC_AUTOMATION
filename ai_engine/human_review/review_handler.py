from langgraph.types import interrupt
from orchestrator.state import State

def human_review_node(state: State):
    stage = state['current_stage']

    output = state[stage] if stage else None

    review_response = interrupt({
        "stage": stage,
        "output": output,
        "message": "Please review the agent output.", 
        "options": ["approve", "revise"]
    })

    decision = review_response['decision']

    if decision not in ['approve', 'revise']:
        raise ValueError("Invalid review decision")
    
    feedback = (
        review_response.get("feedback", "")
        if decision == 'revise'
        else ""
    )

    return {
        'review_decision': decision,
        'review_feedback': feedback
    }