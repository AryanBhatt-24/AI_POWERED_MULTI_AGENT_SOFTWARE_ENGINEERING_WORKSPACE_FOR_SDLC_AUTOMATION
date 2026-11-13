
from llm.model import llm

from agents.architecture_agent.schemas import ArchitectureOutput
from agents.architecture_agent.prompts import ARCHITECTURE_ANALYSIS_PROMPT


def design_architecture(
    requirements: dict,
    feedback: str | None = None,
    reference_context: str | None = None
) -> ArchitectureOutput:

    structured_llm = llm.with_structured_output(ArchitectureOutput)

    prompt = f"""
    {ARCHITECTURE_ANALYSIS_PROMPT}

    Approved Software Requirements:
    {requirements}

    Reference Documents Context:
    {reference_context if reference_context else "No reference documents available."}

    Human Review Feedback:
    {feedback if feedback else "No previous feedback."}

    If feedback is provided:
    - Revise the architecture according to the feedback.
    - Preserve valid existing architectural decisions.
    - Do not introduce contradictions with approved requirements.
    """

    response = structured_llm.invoke(prompt)

    return response
