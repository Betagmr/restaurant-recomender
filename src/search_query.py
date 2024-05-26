import sys

import torch

import chromadb
from src.ranknet.orchestrator import RankerOrchestrator


def search_query(query_text: str, n_results: int = 5):
    db = chromadb.PersistentClient(path="chromadb")
    collection = db.get_collection(name="my_collection")
    query_emb = collection._embed([query_text])

    result = collection.query(
        query_embeddings=query_emb,
        n_results=n_results,
        include=["embeddings", "documents", "metadatas"],
    )

    orchestrator = RankerOrchestrator(
        torch.jit.load("model.pt"),
        query_emb,
        result,
    )

    for restaurant in orchestrator.rank_restaurants():
        print(f"Bar name: {restaurant.name}")
        print(f"street: {restaurant.street}")
        print(f"extra: {restaurant.extra}")
        print(restaurant.content)
        print("----------------------")


if __name__ == "__main__":
    args = sys.argv
    query_text = args[1]
    n_results = int(args[2]) if len(args) > 2 else 5

    search_query(query_text, n_results)
