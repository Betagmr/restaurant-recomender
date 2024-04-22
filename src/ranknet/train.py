import numpy as np
from lightning import Trainer
from lightning.pytorch.loggers import CSVLogger
from torch.utils.data import DataLoader

from src.ranknet.dataset import RankDataset
from src.ranknet.model import RankNet


def train_model():
    # Generate sample data
    n_samples = 50000
    n_features = 450
    data1, data2, target = get_sample_data(n_samples, n_features)

    # Configure training loop
    model = RankNet(n_features)
    logger = CSVLogger("logs", name="ranknet")
    dataset = RankDataset(data1, data2, target)
    loader = DataLoader(dataset, batch_size=256, num_workers=4, shuffle=True)

    trainer = Trainer(
        max_epochs=5_000,
        accelerator="gpu",
        logger=logger,
        accumulate_grad_batches=3,
        deterministic=True,
        enable_progress_bar=False,
    )
    trainer.fit(model, loader)


def get_sample_data(n_samples, n_features):
    rng = np.random.default_rng()

    data1 = rng.random((n_samples, n_features))
    data2 = rng.random((n_samples, n_features))
    target = rng.random((n_samples, 1))

    target = target > 0.5
    target = 1.0 * target

    return data1, data2, target


if __name__ == "__main__":
    train_model()
