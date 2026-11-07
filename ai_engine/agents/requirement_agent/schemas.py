from pydantic import BaseModel, Field

class RequirementOutput(BaseModel):
    project_overview: str = Field(description="Brief overview of the project.")

    functional_requirements: list[str] = Field(description="Features and functionalities the system must provide.")

    non_functional_requirements: list[str] = Field(description="Performance, security, scalability, and usability requirements.")

    constraints: list[str] = Field(description="Technical or business limitation.")

    assumptions: list[str] = Field(description="Assumptions made while analyzing the project.")