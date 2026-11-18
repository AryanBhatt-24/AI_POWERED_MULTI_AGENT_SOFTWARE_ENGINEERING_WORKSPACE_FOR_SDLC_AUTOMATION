
import subprocess
from pathlib import Path


def generate_diagram(
    diagram_source: str,
    output_path: str
) -> dict:
    """
    Save Mermaid source and render it as a PNG image.

    Returns paths of both generated files.
    """

    if not isinstance(diagram_source, str) or not diagram_source.strip():
        raise ValueError("Diagram source must be a non-empty string.")

    output_file = Path(output_path)

    if output_file.suffix.lower() != ".mmd":
        raise ValueError("Diagram source output path must use .mmd extension.")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    output_file.write_text(
        diagram_source,
        encoding="utf-8"
    )

    image_file = output_file.with_suffix(".png")

    command = [
        "npx",
        "--no-install",
        "mmdc",
        "-i",
        str(output_file.resolve()),
        "-o",
        str(image_file.resolve())
    ]

    try:
        subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True
        )

    except FileNotFoundError as exc:
        raise RuntimeError(
            "Mermaid CLI could not be executed. "
            "Verify that Node.js and Mermaid CLI are installed."
        ) from exc

    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Mermaid diagram rendering failed. "
            f"Details: {exc.stderr or exc.stdout}"
        ) from exc

    if not image_file.exists() or image_file.stat().st_size == 0:
        raise RuntimeError(
            "Mermaid CLI did not generate a valid PNG file."
        )

    return {
        "source_path": str(output_file),
        "image_path": str(image_file)
    }
