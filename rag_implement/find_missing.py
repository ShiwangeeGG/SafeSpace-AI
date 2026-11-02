import json
from pathlib import Path
import chromadb

BASE_DIR = Path(__file__).resolve().parent

client = chromadb.PersistentClient(
    path=str(BASE_DIR / "vector_db")
)

collection = client.get_collection("safespace_ai")

with open(BASE_DIR / "chunks" / "all_chunks.json", encoding="utf-8") as f:
    chunks = json.load(f)

stored = set(collection.get(include=[])["ids"])

missing = [
    i for i in range(len(chunks))
    if str(i) not in stored
]

print("Total chunks:", len(chunks))
print("Stored chunks:", collection.count())
print("Missing chunks:", len(missing))

for i in missing:
    chunk = chunks[i]
    print(i, chunk["source"], "| length:", len(chunk["content"] or ""))