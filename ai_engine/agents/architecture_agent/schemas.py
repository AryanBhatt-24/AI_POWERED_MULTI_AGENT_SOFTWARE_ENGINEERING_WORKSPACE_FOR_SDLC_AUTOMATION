from pydantic import BaseModel, Field

class ArchitectureOutput(BaseModel):

    architecture_overview: str = Field(
        description="Detailed system architecture, architectural style, structure, and justification."
    )

    architecture_style: str = Field(
        description="Selected architectural pattern or style and why it fits the project."
    )

    components: list[str] = Field(
        description="Major components, their responsibilities, internal modules, and interactions."
    )

    technology_stack: list[str] = Field(
        description="Recommended technologies, their roles, and technical justification."
    )

    database_design: list[str] = Field(
        description="Database applicability, entities, attributes, relationships, keys, and design justification. Explicitly state N/A if no database is required."
    )

    api_design: list[str] = Field(
        description="Required APIs, endpoints or interfaces, their purpose, inputs, outputs, and integrations. State N/A where not applicable."
    )

    data_flow: list[str] = Field(
        description="Detailed step-by-step data flow across components, including processing and storage."
    )

    component_interactions: list[str] = Field(
        description="Important interactions and communication sequences between system components."
    )

    security_design: list[str] = Field(
        description="Authentication, authorization, data protection, privacy, and other relevant security considerations."
    )

    scalability_and_reliability: list[str] = Field(
        description="Scalability, performance, fault tolerance, availability, and reliability considerations relevant to the project."
    )

    deployment_design: list[str] = Field(
        description="Proposed deployment architecture, infrastructure, runtime environment, and configuration."
    )

    design_decisions: list[str] = Field(
        description="Major technical design decisions, reasons, alternatives considered, and trade-offs."
    )
