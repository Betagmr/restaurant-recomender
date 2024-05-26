from pathlib import Path

import numpy as np

import chromadb
from src.processing.process_data import get_processed_data
from src.processing.vectorize import transform_to_vector_df
from src.utils import load_all_restaurants


def init_db():
    raw_data_path = Path() / "data" / "raw"
    df_raw_restaurants = load_all_restaurants(raw_data_path)
    df_restaurants = get_processed_data(df_raw_restaurants)
    df_vector = transform_to_vector_df(df_raw_restaurants)

    client = chromadb.PersistentClient(path="chromadb")
    db = client.create_collection(name="my_collection")

    metadata = [
        {
            "name": row["bar_name"],
            "street": row["street"],
            "extra": row["extra"],
            "vector": np.array2string(df_vector.iloc[i].to_numpy()[2:])[1:-1],
        }
        for i, row in df_restaurants.iterrows()
    ]

    db.add(
        documents=df_restaurants["search_corpus"].tolist(),
        metadatas=metadata,
        ids=[f"id_{i}" for i in range(len(df_restaurants))],
    )


if __name__ == "__main__":
    init_db()
