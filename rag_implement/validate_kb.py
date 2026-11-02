from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent
KB_PATH = BASE_DIR.parent / "knowledge_base"

bad = []
for f in sorted(Path("../knowledge_base").rglob("*.yaml")):
    try:
        yaml.safe_load(f.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        mark = getattr(e, "context_mark", None) or getattr(e, "problem_mark", None)
        line = mark.line + 1 if mark else "?"
        bad.append(f)
        print(f"{f}  (problem near line {line})")

print(f"\n{len(bad)} files failed to parse")
