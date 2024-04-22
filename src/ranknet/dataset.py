from typing import Any

import torch
from torch import Tensor
from torch.utils.data import Dataset


class RankDataset(Dataset[Any]):
    def __init__(self, data_1, data_2, target) -> None:
        self.data_1 = torch.tensor(data_1, dtype=torch.float32)
        self.data_2 = torch.tensor(data_2, dtype=torch.float32)
        self.target = torch.tensor(target, dtype=torch.float32)

    def __len__(self) -> int:
        return len(self.data_1)

    def __getitem__(self, idx: int) -> tuple[Tensor, Tensor]:
        item_1 = self.data_1[idx]
        item_2 = self.data_2[idx]
        target = self.target[idx]

        return item_1, item_2, target
