import sys

import chromadb


def search_query(query_text: str, n_results: int = 5):
    db = chromadb.PersistentClient(path="chromadb")
    collection = db.get_collection(name="my_collection")

    results = collection.query(
        query_texts=[query_text],
        n_results=n_results,
    )

    result = collection.get(ids=results["ids"][0], include=["documents", "metadatas"])
    for doc, metadata in zip(result["documents"], result["metadatas"]):
        print(f"Bar name: {metadata['name']}")
        print(doc)
        print("----------------------")


if __name__ == "__main__":
    args = sys.argv
    query_text = args[1]
    n_results = int(args[2]) if len(args) > 2 else 5

    search_query(query_text, n_results)
