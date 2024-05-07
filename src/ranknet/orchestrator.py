from dataclasses import dataclass

import torch

from src.ranknet.sorting import merge_sort


class RankerOrchestrator:
    def __init__(self, model, query_emb, results) -> None:
        self.model = model
        self.query_emb = query_emb
        self.sorting = merge_sort
        self.list_restaurants = self._calculate_score(results)

    def _calculate_score(self, results):
        embeddings = results["embeddings"][0]
        metadatas = results["metadatas"][0]
        documents = results["documents"][0]

        list_restaurants = []
        for index in range(len(embeddings)):
            emb = embeddings[index]
            vector = metadatas[index]["vector"]
            restaurant_tensor = torch.tensor(emb + self.query_emb + vector, dtype=torch.float32)

            list_restaurants.append(
                Restaurant(
                    name=metadatas[index]["name"],
                    score=self.model.predict(restaurant_tensor),
                    content=documents[index],
                )
            )

        return list_restaurants

    def rank_restaurants(self):
        return self.sorting(self.list_restaurants, lambda x, y: x.score > y.score)


@dataclass
class Restaurant:
    name: str
    score: float
    content: str
