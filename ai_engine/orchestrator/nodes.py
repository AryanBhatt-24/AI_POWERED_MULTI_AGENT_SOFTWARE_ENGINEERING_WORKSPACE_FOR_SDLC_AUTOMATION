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
    project_id = state["project_id"]

    requirements = state["requirements"]

    # Architecture-focused retrieval query
    retrieval_query = f"""
    Find technical information relevant to designing
    the software architecture.

    Focus on:
    - Existing systems and infrastructure
    - Technology constraints and preferences
    - External integrations
    - Technical requirements
    - Scalability and security considerations

    Project Requirements:
    {requirements}
    """

    # Retrieve relevant project context
    retrieved_documents = retrieve_project_context(
        query=retrieval_query,
        project_id=project_id,
        k=4
    )

    reference_context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    result = design_architecture(
        requirements=requirements,
        feedback=state.get("review_feedback"),
        reference_context=reference_context
    )

    return {
        "architecture": result.model_dump(),
        "current_stage": "architecture",
        "review_decision": None,
        "review_feedback": None
    }


def testing_node(state: State):
    project_id = state["project_id"]

    requirements = state["requirements"]
    architecture = state["architecture"]

    # Testing-focused retrieval query
    retrieval_query = f"""
    Find project information relevant to software testing.

    Focus on:
    - Functional and non-functional validation rules
    - Expected system behavior
    - Technical constraints and limitations
    - Error handling and failure scenarios
    - Edge cases and boundary conditions

    Project Requirements:
    {requirements}

    Software Architecture:
    {architecture}
    """

    retrieved_documents = retrieve_project_context(
        query=retrieval_query,
        project_id=project_id,
        k=4
    )

    reference_context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    result = generate_test_plan(
        requirements=requirements,
        architecture=architecture,
        feedback=state.get("review_feedback"),
        reference_context=reference_context
    )

    return {
        "test_plan": result.model_dump(),
        "current_stage": "testing",
        "review_decision": None,
        "review_feedback": None
    }


def documentation_node(state: State):
    project_id = state["project_id"]

    requirements = state["requirements"]
    architecture = state["architecture"]
    test_plan = state["test_plan"]

    # Documentation-focused retrieval query
    retrieval_query = f"""
    Find project information relevant to preparing
    comprehensive software project documentation.

    Focus on:
    - Project background and objectives
    - Business requirements and project scope
    - Technical specifications and constraints
    - Existing systems and integrations
    - Implementation details and project-specific information

    Project Requirements:
    {requirements}

    Software Architecture:
    {architecture}

    Testing Plan:
    {test_plan}
    """

    retrieved_documents = retrieve_project_context(
        query=retrieval_query,
        project_id=project_id,
        k=4
    )

    reference_context = "\n\n".join(
        document.page_content
        for document in retrieved_documents
    )

    result = generate_documentation(
        requirements=requirements,
        architecture=architecture,
        test_plan=test_plan,
        feedback=state.get("review_feedback"),
        reference_context=reference_context
    )

    return {
        "documentation": result.model_dump(),
        "current_stage": "documentation",
        "review_decision": None,
        "review_feedback": None
    }