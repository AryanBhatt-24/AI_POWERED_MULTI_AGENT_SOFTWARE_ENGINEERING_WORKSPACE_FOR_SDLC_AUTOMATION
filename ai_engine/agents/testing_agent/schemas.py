
from pydantic import BaseModel, Field


class TestCase(BaseModel):
    test_case_id: str = Field(
        description="Unique identifier such as TC-001."
    )

    title: str = Field(
        description="Short and descriptive test case title."
    )

    related_requirement_ids: list[str] = Field(
        default_factory=list,
        description="IDs of related functional or non-functional requirements."
    )

    test_type: str = Field(
        description="Functional, integration, system, security, performance, usability, or other applicable test type."
    )

    priority: str = Field(
        description="Test priority: High, Medium, or Low."
    )

    preconditions: list[str] = Field(default_factory=list)

    test_steps: list[str] = Field(
        default_factory=list,
        description="Ordered steps to execute the test."
    )

    test_data: list[str] = Field(
        default_factory=list,
        description="Required input or test data."
    )

    expected_result: str = Field(
        description="Expected system behavior or outcome."
    )


class TestingOutput(BaseModel):

    testing_overview: str = Field(
        description="Comprehensive testing strategy and overall quality assurance approach."
    )

    testing_levels: list[str] = Field(
        description="Applicable unit, integration, system, acceptance, and other testing levels with their purpose."
    )

    test_cases: list[TestCase] = Field(
        default_factory=list,
        description="Detailed and uniquely identified test cases."
    )

    edge_cases: list[str] = Field(
        default_factory=list,
        description="Boundary conditions, unusual inputs, failure scenarios, and exceptional situations."
    )

    validation_checks: list[str] = Field(
        default_factory=list,
        description="Functional, data integrity, security, and system validation checks."
    )

    test_data_and_environment: list[str] = Field(
        default_factory=list,
        description="Required test data, test environment, tools, and configuration."
    )

    entry_criteria: list[str] = Field(
        default_factory=list,
        description="Conditions that should be satisfied before testing begins."
    )

    exit_criteria: list[str] = Field(
        default_factory=list,
        description="Conditions used to determine whether testing can be considered complete."
    )

    requirement_traceability: list[str] = Field(
        default_factory=list,
        description="Mapping of requirements to corresponding test case IDs and coverage."
    )

    risks_and_limitations: list[str] = Field(
        default_factory=list,
        description="Testing risks, limitations, dependencies, and potential coverage gaps."
    )

    testing_recommendations: list[str] = Field(
        default_factory=list,
        description="Practical recommendations for improving software quality and test coverage."
    )
