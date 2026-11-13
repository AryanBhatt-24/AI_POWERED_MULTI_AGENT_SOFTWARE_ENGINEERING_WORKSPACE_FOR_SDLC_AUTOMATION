
from pydantic import BaseModel, Field


class DocumentationOutput(BaseModel):

    project_title: str = Field(
        description="Professional and accurate title of the software project."
    )

    abstract: str = Field(
        description="Concise overview of the project, its purpose, proposed solution, and expected outcome."
    )

    introduction: str = Field(
        description="Detailed introduction covering project background, problem statement, motivation, objectives, and scope."
    )

    project_scope: list[str] = Field(
        description="Clearly documented in-scope and out-of-scope features, boundaries, and limitations."
    )

    requirements_summary: list[str] = Field(
        description="Detailed summary of functional and non-functional requirements, including their original IDs where available."
    )

    stakeholders_and_use_cases: list[str] = Field(
        description="Relevant stakeholders, their roles, important use cases, actors, and expected interactions."
    )

    business_workflows_and_rules: list[str] = Field(
        description="Important business workflows, process steps, decision points, and business rules."
    )

    constraints_and_assumptions: list[str] = Field(
        description="Documented technical, business, and operational constraints and assumptions."
    )

    architecture_summary: str = Field(
        description="Detailed explanation of the proposed system architecture, architectural style, and overall structure."
    )

    system_components: list[str] = Field(
        description="Major system components, their responsibilities, internal modules, and interactions."
    )

    technology_stack: list[str] = Field(
        description="Technologies, frameworks, libraries, and tools with their roles and justifications. Distinguish confirmed technologies from proposed choices."
    )

    database_and_api_design: list[str] = Field(
        description="Relevant database structures, entities, relationships, APIs, endpoints, interfaces, and integrations. Explicitly mention N/A where not applicable."
    )

    system_workflows_and_data_flow: list[str] = Field(
        description="Step-by-step explanation of important system workflows, data movement, processing, and component communication."
    )

    security_and_reliability: list[str] = Field(
        description="Relevant security, privacy, authentication, authorization, reliability, performance, and scalability considerations."
    )

    deployment_and_configuration: list[str] = Field(
        description="Proposed deployment architecture, runtime environment, infrastructure, configuration, and operational requirements."
    )

    design_decisions_and_tradeoffs: list[str] = Field(
        description="Important architectural and technical decisions, their justifications, alternatives, and trade-offs."
    )

    testing_strategy: str = Field(
        description="Detailed explanation of the overall testing approach, testing levels, testing types, and objectives."
    )

    test_cases_and_validation: list[str] = Field(
        description="Important test cases, their IDs, related requirements, expected results, edge cases, and validation checks."
    )

    testing_criteria_and_risks: list[str] = Field(
        description="Testing entry and exit criteria, test environment, risks, limitations, and unresolved testing dependencies."
    )

    requirement_traceability: list[str] = Field(
        description="Traceability between requirements, architecture components, and test cases wherever the supplied information supports it."
    )

    limitations_and_future_enhancements: list[str] = Field(
        description="Known limitations, unresolved questions, and realistic future enhancement opportunities."
    )

    references_and_source_context: list[str] = Field(
        description="Relevant reference documents and source information actually provided to the agent. Do not invent citations or references."
    )

    conclusion: str = Field(
        description="Comprehensive conclusion summarizing the project objectives, proposed design, testing approach, and expected outcome."
    )
