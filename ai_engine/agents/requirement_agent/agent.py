from llm.model import llm

from agents.requirement_agent.prompts import REQUIREMENT_ANALYSIS_PROMPT
from agents.requirement_agent.schemas import RequirementOutput

def analyze_requirements(
    project_description: str,
    feedback: str | None = None,
    reference_context: str | None = None
) -> RequirementOutput:

    structured_llm = llm.with_structured_output(RequirementOutput)

    prompt = f"""
    {REQUIREMENT_ANALYSIS_PROMPT}

    Project Description:
    {project_description}
    
    Reference Documents Context:
    {reference_context if reference_context else "No reference documents available."}

    Human Review Feedback:
    {feedback if feedback else "No previous feedback."}

    If feedback is provided, revise the requirements
    according to that feedback.
    Preserve all valid existing information.
    """

    response = structured_llm.invoke(prompt)

    return response