from pathlib import Path

import chromadb
from src.processing.process_data import get_processed_data
from src.utils import load_all_restaurants


def init_db():
    raw_data_path = Path() / "data" / "raw"
    df_raw_restaurants = load_all_restaurants(raw_data_path)
    df_restaurants = get_processed_data(df_raw_restaurants)

    client = chromadb.PersistentClient(path="chromadb")
    db = client.create_collection(name="my_collection")
    db.add(
        documents=df_restaurants["search_corpus"].tolist(),
        metadatas=[{"name": name} for name in df_restaurants["bar_name"].tolist()],
        ids=[f"id_{i}" for i in range(len(df_restaurants))],
    )


if __name__ == "__main__":
    init_db()
