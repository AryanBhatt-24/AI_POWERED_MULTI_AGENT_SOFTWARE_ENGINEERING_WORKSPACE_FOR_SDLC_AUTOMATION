
from pydantic import BaseModel, Field


class DocumentationOutput(BaseModel):
    project_title: str = Field(
        description="Title of the software project"
    )

    introduction: str = Field(
        description="Introduction and purpose of the project"
    )

    requirements_summary: str = Field(
        description="Summary of functional and non-functional requirements"
    )

    architecture_summary: str = Field(
        description="Explanation of the proposed system architecture"
    )

    testing_summary: str = Field(
        description="Summary of testing strategy and test cases"
    )

    conclusion: str = Field(
        description="Overall conclusion of the project documentation"
    )
