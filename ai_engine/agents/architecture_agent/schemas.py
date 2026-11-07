from pydantic import BaseModel, Field

class ArchitectureOutput(BaseModel):
    architecture_overview: str = Field(
        description="Overall proposed system architecture"
    )

    components: list[str] = Field(
        description="Major system components and their responsibilities"
    )

    technology_stack: list[str] = Field(
        description="Recommended technologies with their purpose"
    )

    data_flow: list[str] = Field(
        description="Step-by-step flow of data through the system"
    )

    design_decisions: list[str] = Field(
        description="Important architectural decisions and their reasons"
    )

    scalability_considerations: list[str] = Field(
        description="How the architecture can support future growth"
    )