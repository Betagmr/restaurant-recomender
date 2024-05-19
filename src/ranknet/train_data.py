import numpy as np

import chromadb
from src.processing.vectorize import transform_to_vector_df
from src.utils import load_all_restaurants, load_parsed_queries


def get_train_data():
    data = load_all_restaurants("data/raw")
    data = transform_to_vector_df(data)
    result = load_parsed_queries("data/queries.csv", data)

    # Load Bert from ChromaDB
    db = chromadb.PersistentClient(path="chromadb")
    collection = db.get_collection(name="my_collection")

    count = 0
    data_1 = []
    data_2 = []
    for key, content in result.items():
        emb = collection._embed(key)[0]
        list_topic = []

        for row in content.drop(columns=["title"]).to_numpy():
            tensor = np.concatenate([emb, row])
            list_topic.append(tensor)

        data_1.extend(list_topic[1:])
        data_2.extend(list_topic[:-1])

        count += 1
        if count == 50:
            break

    target = np.array([[1] for _ in range(len(data_1))])

    return np.array(data_1), np.array(data_2), target
