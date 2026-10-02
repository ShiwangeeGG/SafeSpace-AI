from pathlib import Path
import yaml
import json


# Path to knowledge base
KB_PATH = Path("../knowledge_base")

# Output folder
CHUNK_PATH = Path("./chunks")
CHUNK_PATH.mkdir(exist_ok=True)


def yaml_to_text(data, indent=0):
    """
    Convert YAML into readable text
    """

    lines = []

    if isinstance(data, dict):

        for k, v in data.items():

            if isinstance(v, (dict, list)):

                lines.append(" " * indent + f"{k}:")

                lines.extend(
                    yaml_to_text(v, indent + 2)
                )

            else:

                lines.append(
                    " " * indent + f"{k}: {v}"
                )

    elif isinstance(data, list):

        for item in data:

            if isinstance(item, (dict, list)):

                lines.extend(
                    yaml_to_text(item, indent + 2)
                )

            else:

                lines.append(
                    " " * indent + f"- {item}"
                )

    return lines


chunks = []

SKIP_FILES = {
    "knowledge_graph.yaml",
    "source_map.yaml",
    "overview.yaml"
}

for file in KB_PATH.rglob("*.yaml"):
    if file.name in SKIP_FILES:
     continue

    try:

        with open(file, "r", encoding="utf-8") as f:

            data = yaml.safe_load(f)

        text = "\n".join(
            yaml_to_text(data)
        )

        chunk = {
            "source": str(file),
            "layer": file.parts[-3] if len(file.parts) >= 3 else "unknown",
            "content": text
        }

        chunks.append(chunk)

        print(f"Loaded: {file}")

    except Exception as e:

        print(f"Error in {file}")
        print(e)


with open(
    CHUNK_PATH / "all_chunks.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        chunks,
        f,
        indent=2,
        ensure_ascii=False
    )

print()
print(f"Created {len(chunks)} chunks")