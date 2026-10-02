import chromadb

client = chromadb.PersistentClient(path="./vector_db")

collection = client.get_collection("safespace_ai")

print("COUNT:", collection.count())