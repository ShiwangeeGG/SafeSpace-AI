from pathlib import Path
import yaml
import json


# Path to knowledge base
BASE_DIR = Path(__file__).resolve().parent

KB_PATH = BASE_DIR.parent / "knowledge_base"
CHUNK_PATH = BASE_DIR / "chunks"

# Output folder
CHUNK_PATH.mkdir(parents=True, exist_ok=True)

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
    "source_info.yaml",
}

for file in sorted(KB_PATH.rglob("*.yaml")):
    if file.name in SKIP_FILES:
     continue

    try:

        with open(file, "r", encoding="utf-8") as f:

            data = yaml.safe_load(f)

            if not data:
               print(f"Skipped empty: {file}")
               continue

        text = yaml.safe_dump(
            data,
            sort_keys=False,
            allow_unicode=True,
            default_flow_style=False
        )

        relative = file.relative_to(KB_PATH)
        layer = relative.parts[0] if len(relative.parts) > 1 else "root"
        if "legal_rules" in relative.parts:
            doc_type = "legal_rules"
        elif "ai_guides" in relative.parts:
            doc_type = "ai_guides"
        else:
            doc_type = "other"

        chunk = {
            "source": relative.as_posix(),
            "layer": layer,
            "category": relative.parts[1] if len(relative.parts) > 1 else "root",
            "doc_type": doc_type,
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