from pathlib import Path
from collections import defaultdict
import yaml

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR.parent / "knowledge_base"

ID_FIELDS = {
    "rule_id",
    "case_id",
    "checklist_id",
    "guide_id",
    "term_id",
    "item_id",
    "section_id",
}

# Required identifiers for file types confirmed from our samples.
# REQUIRED_IDS = {
#     "legal_rules": "rule_id",
#     "case_studies": "case_id",
#     "compliance_rules": "checklist_id",
# }

duplicate_ids = defaultdict(list)
null_fields = []
empty_containers = []
missing_ids = []
parse_errors = []
total_files = 0


def inspect_nested_ids(data, file_path):
    """Find known identifier fields at any nesting level."""

    if isinstance(data, dict):
        for key, value in data.items():

            if key in ID_FIELDS and value is not None:
                duplicate_ids[(key, str(value))].append(str(file_path))

            inspect_nested_ids(value, file_path)

    elif isinstance(data, list):
        for item in data:
            inspect_nested_ids(item, file_path)


def inspect_empty_values(data, file_path, parent=""):
    """Report empty containers and top-level null values."""

    if isinstance(data, dict):
        for key, value in data.items():
            current = f"{parent}.{key}" if parent else key

            if value is None:
                if not parent:
                    null_fields.append((file_path, current))

            elif isinstance(value, (dict, list)):
                if not value:
                    empty_containers.append((file_path, current))

                inspect_empty_values(value, file_path, current)

    elif isinstance(data, list):
        for index, item in enumerate(data):
            inspect_empty_values(item, file_path, f"{parent}[{index}]")


for file_path in sorted(KB_PATH.rglob("*.yaml")):
    total_files += 1

    relative_path = file_path.relative_to(KB_PATH)
    parts = relative_path.parts

    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

    except yaml.YAMLError as error:
        parse_errors.append((file_path, str(error)))
        continue

    if data is None:
        null_fields.append((file_path, "<entire file is empty>"))
        continue

    if not isinstance(data, dict):
        continue

    inspect_nested_ids(data, file_path)
    inspect_empty_values(data, file_path)

    # Check only confirmed file types.
    if "legal_rules" in parts:
        required_id = "rule_id"
    elif (
        parts[0] == "case_studies"
        and file_path.stem.startswith("CASE-")
    ):
        required_id = "case_id"
    elif parts[0] == "compliance_rules":
        required_id = "checklist_id"
    else:
        required_id = None

    if required_id and not data.get(required_id):
        missing_ids.append((file_path, required_id))


# Report duplicate identifiers.
print("\n========== DUPLICATE IDENTIFIERS ==========")

duplicate_count = 0

for (field, value), paths in sorted(duplicate_ids.items()):
    if len(paths) > 1:
        duplicate_count += 1
        print(f"\n{field}: {value}")
        for path in paths:
            print(f"  - {path}")

if duplicate_count == 0:
    print("No duplicate identifiers found.")


# Report top-level null values.
print("\n========== TOP-LEVEL NULL VALUES ==========")

for path, field in null_fields:
    print(f"{path} -> {field}")

if not null_fields:
    print("No top-level null values found.")


# Report empty containers.
print("\n========== EMPTY CONTAINERS ==========")

for path, field in empty_containers:
    print(f"{path} -> {field}")

if not empty_containers:
    print("No empty containers found.")


# Report missing required identifiers.
print("\n========== MISSING REQUIRED IDENTIFIERS ==========")

for path, field in missing_ids:
    print(f"{path} -> missing {field}")

if not missing_ids:
    print("No missing identifiers found in checked file types.")


# Report parsing errors.
print("\n========== YAML PARSE ERRORS ==========")

for path, error in parse_errors:
    print(f"{path}: {error}")

if not parse_errors:
    print("No YAML parsing errors found.")


# Final summary.
print("\n========== AUDIT SUMMARY ==========")
print(f"Total YAML files scanned: {total_files}")
print(f"Duplicate identifier groups: {duplicate_count}")
print(f"Top-level null fields: {len(null_fields)}")
print(f"Empty containers: {len(empty_containers)}")
print(f"Missing required identifiers: {len(missing_ids)}")
print(f"YAML parsing errors: {len(parse_errors)}")
