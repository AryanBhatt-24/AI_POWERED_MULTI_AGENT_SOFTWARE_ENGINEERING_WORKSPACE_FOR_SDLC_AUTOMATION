
from pydantic import BaseModel, Field


class TestingOutput(BaseModel):
    testing_overview: str = Field(
        description="Overall testing strategy for the project"
    )

    test_cases: list[str] = Field(
        description="Test cases covering major functionalities"
    )

    edge_cases: list[str] = Field(
        description="Important edge cases that need testing"
    )

    validation_checks: list[str] = Field(
        description="Checks to validate system behavior and correctness"
    )

    testing_recommendations: list[str] = Field(
        description="Recommendations for improving software quality"
    )
