from orchestrator.state import State
from agents.requirement_agent.agent import analyze_requirements
from agents.architecture_agent.agent import design_architecture
from agents.testing_agent.agent import generate_test_plan
from agents.documentation_agent.agent import generate_documentation
from ai_engine.rag.pipeline import retrieve_project_context

def requirement_node(state: State):
    project_id = state["project_id"]

    # Retrieve relevant context from uploaded project documents
    retrieved_documents = retrieve_project_context(
        query=state["user_input"],
        project_id=project_id,
        k=4
    )

    # Convert retrieved documents into a single context string
    reference_context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    result = analyze_requirements(
        project_description=state["user_input"],
        feedback=state.get("review_feedback"),
        reference_context=reference_context
    )

    return {
        "requirements": result.model_dump(),
        "current_stage": "requirements",
        "review_decision": None,
        "review_feedback": None
    }

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