import sys

import chromadb


def search_query(query_text: str, n_results: int = 5):
    db = chromadb.PersistentClient(path="chromadb")
    collection = db.get_collection(name="my_collection")
    query_emb = collection._embed([query_text])

    result = collection.query(
        query_embeddings=query_emb,
        n_results=n_results,
        include=["embeddings", "documents", "metadatas"],
    )

    for doc, metadata in zip(result["documents"][0], result["metadatas"][0]):
        print(f"Bar name: {metadata['name']}")
        print(doc)
        print("----------------------")


if __name__ == "__main__":
    args = sys.argv
    query_text = args[1]
    n_results = int(args[2]) if len(args) > 2 else 5

    search_query(query_text, n_results)
