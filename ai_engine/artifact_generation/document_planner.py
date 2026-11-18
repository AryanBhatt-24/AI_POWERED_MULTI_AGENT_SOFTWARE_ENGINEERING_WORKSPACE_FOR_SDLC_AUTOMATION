import json
from typing import Literal

from pydantic import BaseModel, Field

from llm.model import llm

# ==================================================
# DOCUMENT PLAN SCHEMAS
# ==================================================

class PlannedContentBlock(BaseModel):
    """
    References one original top-level field
    from an approved agent output.
    """

    source_field: str = Field(
        description=(
            "Exact top-level key from the original agent output. "
            "Do not rename or invent source fields."
        )
    )

    heading: str = Field(
        description="Professional heading for this content."
    )

    presentation: Literal[
        "paragraph",
        "bullet_list",
        "numbered_list",
        "table",
        "structured"
    ] = Field(
        description=(
            "Suitable presentation format for the referenced "
            "source field."
        )
    )


class PlannedSection(BaseModel):
    """One major section of the generated document."""

    title: str

    purpose: str

    content_blocks: list[PlannedContentBlock] = Field(
        default_factory=list
    )


class DocumentPlan(BaseModel):
    """Structured document arrangement returned by the LLM."""

    document_title: str

    document_subtitle: str | None = None

    sections: list[PlannedSection]


# ==================================================
# AGENT CONFIGURATION
# ==================================================

AGENT_LABELS = {
    "requirements": "Requirements Analysis",
    "architecture": "Architecture and Design",
    "test_plan": "Software Testing",
    "documentation": "Project Documentation"
}


# ==================================================
# SOURCE NORMALIZATION
# ==================================================

def normalize_agent_output(agent_output: dict) -> dict:
    """
    Ensure the source is a dictionary.

    Agent nodes already use model_dump(), but this
    also supports Pydantic objects during testing.
    """

    if isinstance(agent_output, dict):
        return agent_output

    if hasattr(agent_output, "model_dump"):
        return agent_output.model_dump()

    raise TypeError(
        "Agent output must be a dictionary or Pydantic model."
    )


def has_content(value) -> bool:
    """
    Determine whether a source field contains
    meaningful content.

    Empty containers and None are excluded.
    Numeric zero and False remain valid values.
    """

    if value is None:
        return False

    if isinstance(value, str):
        return bool(value.strip())

    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0

    return True


def build_source_catalog(agent_output: dict):
    """
    Create a catalog of original source fields.

    Actual source content remains in agent_output.
    The catalog is used only for document planning.
    """

    catalog = []
    empty_fields = []

    for field_name, value in agent_output.items():

        if not has_content(value):
            empty_fields.append(field_name)
            continue

        serialized_value = json.dumps(
            value,
            ensure_ascii=False,
            default=str
        )

        # Limit preview size to control prompt length.
        preview = serialized_value[:700]

        if len(serialized_value) > 700:
            preview += "... [preview truncated]"

        if isinstance(value, dict):
            value_type = "object"

        elif isinstance(value, list):
            value_type = "array"

        else:
            value_type = type(value).__name__

        catalog.append({
            "source_field": field_name,
            "value_type": value_type,
            "preview": preview
        })

    if not catalog:
        raise ValueError(
            "Agent output contains no non-empty fields."
        )

    return catalog, empty_fields


# ==================================================
# PRESENTATION VALIDATION
# ==================================================

def validate_presentation(
    presentation: str,
    value,
    source_field: str
):
    """
    Ensure the selected presentation is compatible
    with the original source data.
    """

    allowed_presentations = {
        "paragraph",
        "bullet_list",
        "numbered_list",
        "table",
        "structured"
    }

    if presentation not in allowed_presentations:
        raise ValueError(
            f"Unsupported presentation '{presentation}'. "
            f"Allowed formats: {sorted(allowed_presentations)}"
        )

    is_scalar = not isinstance(value, (dict, list))

    if presentation == "paragraph" and not is_scalar:
        raise ValueError(
            f"Field '{source_field}' is not scalar "
            "and cannot use paragraph presentation."
        )

    if presentation in {"bullet_list", "numbered_list"}:

        if not isinstance(value, list):
            raise ValueError(
                f"Field '{source_field}' must be a list."
            )

        if any(
            isinstance(item, (dict, list))
            for item in value
        ):
            raise ValueError(
                f"Field '{source_field}' contains nested data. "
                "Use structured or table presentation."
            )

    if presentation == "table":

        if not isinstance(value, list) or not value:
            raise ValueError(
                f"Field '{source_field}' is not a valid table."
            )

        if not all(isinstance(item, dict) for item in value):
            raise ValueError(
                f"Field '{source_field}' must contain objects "
                "for table presentation."
            )

        expected_keys = set(value[0].keys())

        if not all(
            set(item.keys()) == expected_keys
            for item in value
        ):
            raise ValueError(
                f"Field '{source_field}' has inconsistent "
                "table columns."
            )

    if presentation == "structured":

        if not isinstance(value, (dict, list)):
            raise ValueError(
                f"Field '{source_field}' is scalar "
                "and cannot use structured presentation."
            )


# ==================================================
# DOCUMENT PLAN VALIDATION
# ==================================================

def validate_document_plan(
    plan: DocumentPlan,
    agent_output: dict,
    catalog: list
):
    """
    Validate the plan against the original source.

    Every non-empty top-level source field must appear
    exactly once in the document plan.
    """

    if not plan.sections:
        raise ValueError(
            "Document plan contains no sections."
        )

    expected_fields = {
        item["source_field"]
        for item in catalog
    }

    used_fields = []

    for section in plan.sections:

        if not section.content_blocks:
            raise ValueError(
                f"Section '{section.title}' has no content."
            )

        for block in section.content_blocks:

            source_field = block.source_field

            if source_field not in agent_output:
                raise ValueError(
                    f"Unknown source field: {source_field}"
                )

            if source_field not in expected_fields:
                raise ValueError(
                    f"Source field '{source_field}' "
                    "is empty or unavailable."
                )

            validate_presentation(
                presentation=block.presentation,
                value=agent_output[source_field],
                source_field=source_field
            )

            used_fields.append(source_field)

    # Reject duplicate source references.
    duplicates = {
        field
        for field in used_fields
        if used_fields.count(field) > 1
    }

    if duplicates:
        raise ValueError(
            f"Duplicate source fields: {sorted(duplicates)}"
        )

    # Reject omitted source fields.
    missing_fields = expected_fields - set(used_fields)

    if missing_fields:
        raise ValueError(
            "Document plan omitted source fields: "
            f"{sorted(missing_fields)}"
        )

    return plan


# ==================================================
# DOCUMENT PLANNER
# ==================================================

def create_document_plan(
    agent_name: str,
    agent_output: dict,
    project_title: str | None = None
) -> dict:
    """
    Create a document plan for one approved agent output.

    Supported agent names:
        requirements
        architecture
        test_plan
        documentation

    The LLM organizes content but does not rewrite
    the original technical information.
    """

    if agent_name not in AGENT_LABELS:
        raise ValueError(
            f"Unsupported agent name: {agent_name}"
        )

    agent_output = normalize_agent_output(agent_output)

    catalog, empty_fields = build_source_catalog(
        agent_output
    )

    agent_label = AGENT_LABELS[agent_name]

    if not project_title:
        project_title = agent_output.get(
            "project_title",
            "Software Project"
        )

    source_catalog = json.dumps(
        catalog,
        indent=2,
        ensure_ascii=False
    )

    prompt = f"""
You are a professional software documentation architect.

Prepare a structured document plan for:

Project: {project_title}

Document Type: {agent_label}

SOURCE FIELD CATALOG:
{source_catalog}

YOUR RESPONSIBILITY:

Organize the available source fields into a professional,
comprehensive technical document.

STRICT RULES:

1. Use only the exact source_field names provided
   in the source catalog.

2. Every non-empty source field must appear exactly once
   in the final document plan.

3. Do not omit, rename, merge, or duplicate source fields.

4. Do not rewrite, summarize, or replace original content.

5. The document builder will retrieve the original content
   directly from the source dictionary.

6. Arrange related information into logical sections
   and subsections.

7. Maintain a meaningful progression of topics.

8. Preserve technical terminology and original identifiers.

9. Choose presentation formats according to the actual
   source data types:

   - paragraph: scalar text or values.
   - bullet_list: list of scalar items.
   - numbered_list: ordered list of scalar items.
   - table: list of objects having identical keys.
   - structured: nested dictionaries or nested lists.

10. Do not use table presentation for incompatible data.

11. Do not invent project facts, features, requirements,
    technologies, test results, or design decisions.

12. Section titles and headings may be professionally
    worded, but must not introduce new technical claims.

13. Avoid unnecessary repetition.

14. Preserve the original information's technical depth.

15. Do not create diagram content. Diagram generation
    is handled separately using supported source material.

Return a DocumentPlan matching the supplied schema.
"""

    structured_llm = llm.with_structured_output(
        DocumentPlan
    )

    response = structured_llm.invoke(prompt)

    plan = DocumentPlan.model_validate(response)

    validate_document_plan(
        plan=plan,
        agent_output=agent_output,
        catalog=catalog
    )

    result = plan.model_dump()

    # Keep a traceable record of source coverage.
    result["source_agent"] = agent_name

    result["covered_source_fields"] = [
        item["source_field"]
        for item in catalog
    ]

    result["empty_source_fields"] = empty_fields

    return result
