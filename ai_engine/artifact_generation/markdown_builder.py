from pathlib import Path
from datetime import datetime

def build_markdown(
    title: str,
    content: dict,
    output_path: str
) -> str:

    """
    Convert an agent's approved structured output
    into an editable Markdown document.
    """

    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# {title}",
        "",
        f"Generated on: {datetime.now().strftime('%d %B %Y')}",
        "",
        "---",
        ""
    ]
    
    def add_section(key: str, value):
        heading = key.replace("_", " ").title()
        lines.append(f"## {heading}")
        lines.append("")

        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    for sub_key, sub_value in item.items():
                        lines.append(
                            f"- **{sub_key.replace('_', ' ').title()}:** "
                            f"{sub_value}"
                        )
                else:
                    lines.append(f"- {item}")

        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                lines.append(
                    f"- **{sub_key.replace('_', ' ').title()}:** "
                    f"{sub_value}"
                )

        else:
            lines.append(str(value))

        lines.append("")

    for key, value in content.items():
        if value is not None:
            add_section(key, value)

    output_file.write_text(
        "\n".join(lines),
        encoding="utf-8"
    )

    return str(output_file)