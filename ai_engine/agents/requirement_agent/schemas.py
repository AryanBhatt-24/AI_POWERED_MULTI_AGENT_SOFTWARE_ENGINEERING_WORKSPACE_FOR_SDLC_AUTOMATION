from typing import Literal
from pydantic import BaseModel, Field

class ProjectScope(BaseModel):
    in_scope: list[str] = Field(
        default_factory=list,
        description="Features, functionalities, and objectives included in the project."
    )

    out_of_scope: list[str] = Field(
        default_factory=list,
        description="Features and functionalities explicitly excluded from the project."
    )


class Stakeholder(BaseModel):
    name: str = Field(description="Stakeholder or user role.")

    role: str = Field(description="Role and responsibilities of the stakeholder.")

    goals: list[str] = Field(
        default_factory=list,
        description="Goals and expectations of this stakeholder."
    )


class FunctionalRequirement(BaseModel):
    requirement_id: str = Field(
        description="Unique identifier, such as FR-001."
    )

    title: str = Field(description="Short requirement title.")

    description: str = Field(
        description="Detailed description of the required system functionality."
    )

    priority: Literal["High", "Medium", "Low"] = Field(
        description="Business priority of the requirement."
    )

    acceptance_criteria: list[str] = Field(
        default_factory=list,
        description="Specific conditions that must be satisfied for this requirement to be accepted."
    )

    dependencies: list[str] = Field(
        default_factory=list,
        description="IDs of other requirements this requirement depends on."
    )


class NonFunctionalRequirement(BaseModel):
    requirement_id: str = Field(
        description="Unique identifier, such as NFR-001."
    )

    category: str = Field(
        description="Category such as performance, security, reliability, or usability."
    )

    description: str = Field(
        description="Detailed description of the quality requirement."
    )

    measurable_target: str = Field(
        description="Measurable target or expected quality level, when applicable."
    )

    verification_method: str = Field(
        description="How the requirement can be verified or evaluated."
    )


class UseCase(BaseModel):
    use_case_id: str = Field(description="Unique use-case identifier.")

    title: str = Field(description="Use-case name.")

    description: str = Field(description="Purpose of the use case.")

    primary_actor: str = Field(description="Main actor performing the use case.")

    preconditions: list[str] = Field(default_factory=list)

    main_flow: list[str] = Field(
        default_factory=list,
        description="Normal sequence of steps."
    )

    alternative_flows: list[str] = Field(default_factory=list)

    exception_flows: list[str] = Field(default_factory=list)

    postconditions: list[str] = Field(default_factory=list)

    related_requirement_ids: list[str] = Field(default_factory=list)


class BusinessWorkflow(BaseModel):
    workflow_id: str = Field(description="Unique workflow identifier.")

    name: str = Field(description="Workflow name.")

    description: str = Field(description="Purpose of the business workflow.")

    trigger: str = Field(description="Event or condition that starts the workflow.")

    steps: list[str] = Field(
        default_factory=list,
        description="Ordered steps in the workflow."
    )

    decision_points: list[str] = Field(
        default_factory=list,
        description="Important decisions and their possible outcomes."
    )

    related_requirement_ids: list[str] = Field(default_factory=list)


class BusinessRule(BaseModel):
    rule_id: str = Field(description="Unique business rule identifier.")

    description: str = Field(
        description="A domain-specific rule or condition the system must follow."
    )

    related_requirement_ids: list[str] = Field(default_factory=list)


class RequirementTraceability(BaseModel):
    requirement_id: str = Field(
        description="ID of the requirement being traced."
    )

    related_use_case_ids: list[str] = Field(default_factory=list)

    acceptance_criteria: list[str] = Field(default_factory=list)

    verification_notes: str = Field(
        description="How this requirement will be verified."
    )


class RequirementOutput(BaseModel):
    project_overview: str = Field(
        description="Comprehensive overview of the project, its problem, objectives, and proposed solution."
    )

    project_scope: ProjectScope = Field(
        description="Project boundaries, included and excluded functionalities."
    )

    stakeholders: list[Stakeholder] = Field(default_factory=list)

    functional_requirements: list[FunctionalRequirement] = Field(
        default_factory=list
    )

    non_functional_requirements: list[NonFunctionalRequirement] = Field(
        default_factory=list
    )

    use_cases: list[UseCase] = Field(default_factory=list)

    business_workflows: list[BusinessWorkflow] = Field(default_factory=list)

    business_rules: list[BusinessRule] = Field(default_factory=list)

    constraints: list[str] = Field(default_factory=list)

    assumptions: list[str] = Field(default_factory=list)

    requirement_traceability: list[RequirementTraceability] = Field(
        default_factory=list
    )

    open_questions: list[str] = Field(
        default_factory=list,
        description="Ambiguities, missing information, and questions requiring stakeholder clarification."
    )
