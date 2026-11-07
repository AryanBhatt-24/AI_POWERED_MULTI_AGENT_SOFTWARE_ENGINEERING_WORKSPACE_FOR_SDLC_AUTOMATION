from orchestrator.state import State
from agents.requirement_agent.agent import analyze_requirements
from agents.architecture_agent.agent import design_architecture
from agents.testing_agent.agent import generate_test_plan
from agents.documentation_agent.agent import generate_documentation

def requirement_node(state: State):
    result = analyze_requirements(state['user_input'], state["review_feedback"])
    return {'requirements': result.model_dump(), "current_stage": "requirements"}

def architecture_node(state: State):
    result = design_architecture(state["requirements"], state["review_feedback"])
    return {"architecture": result.model_dump(), "current_stage": "architecture"}


def testing_node(state: State):
    result = generate_test_plan(
        state["requirements"],
        state["architecture"],
        state["review_feedback"]
    )
    return {"test_plan": result.model_dump(), "current_stage": "test_plan"}


def documentation_node(state: State):
    result = generate_documentation(
        state["requirements"],
        state["architecture"],
        state["test_plan"],
        state["review_feedback"]
    )
    return {"documentation": result.model_dump(), "current_stage": "documentation"}