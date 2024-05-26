from dataclasses import dataclass

import numpy as np
import torch

from src.ranknet.sorting import merge_sort


@dataclass
class Restaurant:
    name: str
    score: float
    content: str
    street: str
    extra: str


class RankerOrchestrator:
    def __init__(self, model, query_emb, results) -> None:
        self.model = model
        self.query_emb = query_emb[0]
        self.sorting = merge_sort
        self.list_restaurants = self._calculate_score(results)

    def _calculate_score(self, results):
        metadatas = results["metadatas"][0]
        documents = results["documents"][0]

        list_restaurants = []
        for index in range(len(documents)):
            vector = np.fromstring(metadatas[index]["vector"], sep=" ", dtype=int)
            tensor = self.query_emb + vector.tolist()
            restaurant_tensor = torch.tensor(tensor, dtype=torch.float32)

            list_restaurants.append(
                Restaurant(
                    name=metadatas[index]["name"],
                    score=self.model.predict(restaurant_tensor),
                    content=documents[index],
                    street=metadatas[index]["street"],
                    extra=metadatas[index]["extra"] if "extra" in metadatas[index] else "N/A",
                )
            )

        return list_restaurants

    def rank_restaurants(self) -> list[Restaurant]:
        return self.sorting(self.list_restaurants, lambda x, y: x.score > y.score)
