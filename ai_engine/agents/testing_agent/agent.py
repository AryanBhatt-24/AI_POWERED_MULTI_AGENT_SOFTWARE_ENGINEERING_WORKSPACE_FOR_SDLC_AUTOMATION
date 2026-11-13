
from llm.model import llm

from agents.testing_agent.schemas import TestingOutput
from agents.testing_agent.prompts import TESTING_ANALYSIS_PROMPT

def generate_test_plan(
    requirements: dict,
    architecture: dict,
    feedback: str | None = None,
    reference_context: str | None = None
) -> TestingOutput:

    structured_llm = llm.with_structured_output(TestingOutput)

    prompt = f"""
    {TESTING_ANALYSIS_PROMPT}

    Software Requirements:
    {requirements}

    Software Architecture:
    {architecture}

    Reference Documents Context:
    {reference_context if reference_context else "No reference documents available."}

    Human Review Feedback:
    {feedback if feedback else "No previous feedback."}

    If feedback is provided, revise the testing plan
    according to that feedback while preserving valid test cases.
    """

    response = structured_llm.invoke(prompt)

    return response