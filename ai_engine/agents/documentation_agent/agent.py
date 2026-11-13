
from llm.model import llm

from agents.documentation_agent.schemas import DocumentationOutput
from agents.documentation_agent.prompts import DOCUMENTATION_PROMPT

def generate_documentation(
    requirements: dict,
    architecture: dict,
    test_plan: dict,
    feedback: str | None = None,
    reference_context: str | None = None
) -> DocumentationOutput:

    structured_llm = llm.with_structured_output(DocumentationOutput)

    prompt = f"""
    {DOCUMENTATION_PROMPT}

    Requirements:
    {requirements}

    Architecture:
    {architecture}

    Testing Plan:
    {test_plan}

    Reference Documents Context:
    {reference_context if reference_context else "No reference documents available."}
    
    Human Review Feedback:
    {feedback if feedback else "No previous feedback."}

    If feedback is provided, revise the documentation
    according to that feedback while preserving valid information.
    """

    response = structured_llm.invoke(prompt)

    return response