from typing import Any
from .document_planner import has_content
from .markdown_builder import build_markdown
from .pdf_builder import build_pdf
from xml.sax.saxutils import escape
import re
from pathlib import Path
from .diagram_generator import generate_diagram
from .document_planner import create_document_plan

def prepare_document_sections(
    plan: dict,
    agent_output: dict
) -> list[dict]:
    """
    Map a validated document plan to the original agent content.

    The original agent output remains unchanged.
    Each planned content block retains its source field,
    heading, presentation format and original content.
    """

    if not isinstance(plan, dict):
        raise TypeError("Document plan must be a dictionary.")

    if not isinstance(agent_output, dict):
        raise TypeError("Agent output must be a dictionary.")

    planned_sections = plan.get("sections")

    if not isinstance(planned_sections, list) or not planned_sections:
        raise ValueError(
            "Document plan must contain non-empty sections."
        )

    document_sections = []
    covered_fields = set()

    for section in planned_sections:

        if not isinstance(section, dict):
            raise ValueError(
                "Each planned section must be a dictionary."
            )

        section_title = section.get("title")
        section_purpose = section.get("purpose", "")

        if not isinstance(section_title, str) or not section_title.strip():
            raise ValueError(
                "Every planned section must have a title."
            )

        content_blocks = section.get("content_blocks")

        if not isinstance(content_blocks, list) or not content_blocks:
            raise ValueError(
                f"Section '{section_title}' has no content blocks."
            )

        for block in content_blocks:

            if not isinstance(block, dict):
                raise ValueError(
                    f"Invalid content block in section '{section_title}'."
                )

            source_field = block.get("source_field")
            heading = block.get("heading")
            presentation = block.get("presentation")

            if not isinstance(source_field, str) or not source_field:
                raise ValueError(
                    "Content block has an invalid source field."
                )

            if source_field in covered_fields:
                raise ValueError(
                    f"Duplicate source field: '{source_field}'."
                )

            if source_field not in agent_output:
                raise ValueError(
                    f"Source field '{source_field}' does not exist "
                    "in the original agent output."
                )

            original_content = agent_output[source_field]

            if not has_content(original_content):
                raise ValueError(
                    f"Source field '{source_field}' contains no content."
                )

            if not isinstance(heading, str) or not heading.strip():
                raise ValueError(
                    f"Source field '{source_field}' has an invalid heading."
                )

            if presentation not in {
                "paragraph",
                "bullet_list",
                "numbered_list",
                "table",
                "structured"
            }:
                raise ValueError(
                    f"Unsupported presentation '{presentation}' "
                    f"for source field '{source_field}'."
                )

            document_sections.append({
                "section_title": section_title,
                "section_purpose": section_purpose,
                "heading": heading,
                "source_field": source_field,
                "presentation": presentation,
                "content": original_content
            })

            covered_fields.add(source_field)

    return document_sections


def generate_markdown_document(
    title: str,
    document_sections: list[dict],
    output_path: str
) -> str:
    """
    Generate an editable Markdown document from
    prepared document sections.

    Preserves the planned section order and original content.
    """

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Document title must be a non-empty string.")

    if not isinstance(document_sections, list) or not document_sections:
        raise ValueError("Document sections must be a non-empty list.")

    content = {}

    for section in document_sections:

        if not isinstance(section, dict):
            raise ValueError("Each document section must be a dictionary.")

        section_title = section.get("section_title")
        heading = section.get("heading")
        source_field = section.get("source_field")
        original_content = section.get("content")

        if not isinstance(section_title, str) or not section_title.strip():
            raise ValueError("Every section must have a valid section title.")

        if not isinstance(heading, str) or not heading.strip():
            raise ValueError("Every section must have a valid heading.")

        if not isinstance(source_field, str) or not source_field.strip():
            raise ValueError("Every section must have a valid source field.")

        if not has_content(original_content):
            raise ValueError(
                f"Source field '{source_field}' contains no content."
            )

        if section_title not in content:
            content[section_title] = {}

        if heading in content[section_title]:
            raise ValueError(
                f"Duplicate heading '{heading}' "
                f"inside section '{section_title}'."
            )

        content[section_title][heading] = original_content

    return build_markdown(
        title=title,
        content=content,
        output_path=output_path
    )


def _format_pdf_value(value: Any, prefix: str = "") -> list[str]:
    """
    Convert nested dictionaries and lists into readable
    PDF bullet items without discarding original information.
    """

    formatted_items = []

    if isinstance(value, dict):

        for key, sub_value in value.items():

            label = str(key).replace("_", " ").title()

            if isinstance(sub_value, (dict, list)):
                formatted_items.extend(
                    _format_pdf_value(
                        sub_value,
                        prefix=f"{prefix}{label} - "
                    )
                )
            else:
                formatted_items.append(
                    f"{prefix}{label}: {escape(str(sub_value))}"
                )

    elif isinstance(value, list):

        for index, item in enumerate(value, start=1):

            if isinstance(item, (dict, list)):
                formatted_items.extend(
                    _format_pdf_value(
                        item,
                        prefix=f"{prefix}Item {index} - "
                    )
                )
            else:
                formatted_items.append(
                    f"{prefix}{escape(str(item))}"
                )

    else:
        formatted_items.append(
            f"{prefix}{escape(str(value))}"
        )

    return formatted_items


def attach_diagrams_to_sections(
    document_sections: list[dict],
    diagrams: list[dict],
    output_dir: str
) -> list[dict]:
    """
    Generate Mermaid diagrams and associate them with
    their corresponding document sections.

    Each diagram targets one section using section_title.
    Original document content remains unchanged.
    """

    if not isinstance(document_sections, list) or not document_sections:
        raise ValueError(
            "Document sections must be a non-empty list."
        )

    if not isinstance(diagrams, list):
        raise TypeError("Diagrams must be provided as a list.")

    if not isinstance(output_dir, str) or not output_dir.strip():
        raise ValueError("Output directory must be a non-empty string.")

    section_map = {}

    for section in document_sections:

        if not isinstance(section, dict):
            raise ValueError(
                "Each document section must be a dictionary."
            )

        section_title = section.get("section_title")

        if not isinstance(section_title, str) or not section_title.strip():
            raise ValueError(
                "Every document section must have a valid title."
            )

        if section_title in section_map:
            raise ValueError(
                f"Duplicate document section: '{section_title}'."
            )

        section_map[section_title] = section

    prepared_diagrams = set()
    output_root = Path(output_dir)

    for diagram in diagrams:

        if not isinstance(diagram, dict):
            raise ValueError(
                "Each diagram definition must be a dictionary."
            )

        section_title = diagram.get("section_title")
        diagram_name = diagram.get("diagram_name")
        diagram_source = diagram.get("diagram_source")

        if not isinstance(section_title, str) or not section_title.strip():
            raise ValueError(
                "Diagram must specify a valid section title."
            )

        if section_title not in section_map:
            raise ValueError(
                f"Target section '{section_title}' does not exist."
            )

        if section_title in prepared_diagrams:
            raise ValueError(
                f"A diagram is already associated with "
                f"section '{section_title}'."
            )

        if not isinstance(diagram_name, str) or not diagram_name.strip():
            raise ValueError(
                "Diagram name must be a non-empty string."
            )

        if not isinstance(diagram_source, str) or not diagram_source.strip():
            raise ValueError(
                f"Diagram source for '{diagram_name}' is empty."
            )

        # Generate a filesystem-safe filename.
        safe_name = re.sub(
            r"[^a-zA-Z0-9_-]+",
            "_",
            diagram_name.strip()
        ).strip("_")

        if not safe_name:
            raise ValueError("Diagram name is not a valid filename.")

        diagram_path = output_root / "diagrams" / f"{safe_name}.mmd"

        generated = generate_diagram(
            diagram_source=diagram_source,
            output_path=str(diagram_path)
        )

        section = section_map[section_title]

        section["diagram_path"] = generated["image_path"]
        section["diagram_source_path"] = generated["source_path"]

        prepared_diagrams.add(section_title)

    return document_sections

def generate_pdf_document(
    title: str,
    document_sections: list[dict],
    output_path: str
) -> str:
    """
    Generate a PDF document from prepared document sections.

    Converts planned sections into the format expected by
    the existing PDF Builder.
    """

    if not isinstance(title, str) or not title.strip():
        raise ValueError(
            "Document title must be a non-empty string."
        )

    if not isinstance(document_sections, list) or not document_sections:
        raise ValueError(
            "Document sections must be a non-empty list."
        )

    pdf_sections = []

    for section in document_sections:

        if not isinstance(section, dict):
            raise ValueError(
                "Each document section must be a dictionary."
            )

        section_title = section.get("section_title")
        heading = section.get("heading")
        source_field = section.get("source_field")
        presentation = section.get("presentation")
        original_content = section.get("content")

        if not isinstance(section_title, str) or not section_title.strip():
            raise ValueError(
                "Every section must have a valid section title."
            )

        if not isinstance(heading, str) or not heading.strip():
            raise ValueError(
                "Every section must have a valid heading."
            )

        if not isinstance(source_field, str) or not source_field.strip():
            raise ValueError(
                "Every section must have a valid source field."
            )

        if not has_content(original_content):
            raise ValueError(
                f"Source field '{source_field}' contains no content."
            )

        if presentation not in {
            "paragraph",
            "bullet_list",
            "numbered_list",
            "table",
            "structured"
        }:
            raise ValueError(
                f"Unsupported presentation '{presentation}'."
            )

        if presentation == "paragraph":
            pdf_content = escape(str(original_content))
        else:
            pdf_content = _format_pdf_value(original_content)

        pdf_sections.append({
            "heading": (
                f"{escape(section_title)} - {escape(heading)}"
            ),
            "content": pdf_content,
            "diagram_path": section.get("diagram_path")
        })

    generated_path = build_pdf(
        title=escape(title),
        sections=pdf_sections,
        output_path=output_path
    )

    return generated_path


def generate_agent_artifacts(
    agent_name: str,
    agent_output: dict,
    output_root: str,
    project_title: str | None = None,
    diagrams: list[dict] | None = None
) -> dict:
    """
    Execute the complete artifact generation workflow
    for one approved agent output.

    Generates:
    - A structured document plan
    - Prepared document sections
    - An editable Markdown document
    - Relevant Mermaid diagrams
    - A PDF document

    Returns paths and metadata for generated artifacts.
    """

    if not isinstance(agent_name, str) or not agent_name.strip():
        raise ValueError("Agent name must be a non-empty string.")

    if not isinstance(agent_output, dict):
        raise TypeError("Agent output must be a dictionary.")

    if not isinstance(output_root, str) or not output_root.strip():
        raise ValueError("Output root must be a non-empty string.")

    if diagrams is not None and not isinstance(diagrams, list):
        raise TypeError("Diagrams must be a list or None.")

    # Step 1: Generate document plan.
    plan = create_document_plan(
        agent_name=agent_name,
        agent_output=agent_output,
        project_title=project_title
    )

    document_title = plan.get("document_title")

    if not isinstance(document_title, str) or not document_title.strip():
        raise ValueError("Document planner returned an invalid title.")

    # Step 2: Map original agent output to planned sections.
    document_sections = prepare_document_sections(
        plan=plan,
        agent_output=agent_output
    )

    # Step 3: Prepare agent-specific output directory.
    agent_directory = Path(output_root) / agent_name
    agent_directory.mkdir(parents=True, exist_ok=True)

    markdown_path = agent_directory / "document.md"
    pdf_path = agent_directory / "document.pdf"

    # Step 4: Generate and associate diagrams.
    if diagrams:
        document_sections = attach_diagrams_to_sections(
            document_sections=document_sections,
            diagrams=diagrams,
            output_dir=str(agent_directory)
        )

    # Step 5: Generate editable Markdown.
    generated_markdown = generate_markdown_document(
        title=document_title,
        document_sections=document_sections,
        output_path=str(markdown_path)
    )

    # Step 6: Generate PDF.
    generated_pdf = generate_pdf_document(
        title=document_title,
        document_sections=document_sections,
        output_path=str(pdf_path)
    )

    # Step 7: Collect diagram metadata.
    generated_diagrams = []

    for section in document_sections:
        if section.get("diagram_path"):
            generated_diagrams.append({
                "section_title": section["section_title"],
                "diagram_path": section["diagram_path"],
                "diagram_source_path": section.get(
                    "diagram_source_path"
                )
            })

    return {
        "agent_name": agent_name,
        "document_title": document_title,
        "document_plan": plan,
        "markdown_path": generated_markdown,
        "pdf_path": generated_pdf,
        "diagrams": generated_diagrams,
        "output_directory": str(agent_directory)
    }
