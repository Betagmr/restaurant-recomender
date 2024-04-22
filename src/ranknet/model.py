from time import time

from lightning import LightningModule
from torch import nn
from torch.optim import Adam
from tqdm import tqdm


class RankNet(LightningModule):
    def __init__(self, n_features, lr=1e-3, loss=nn.BCELoss):
        super().__init__()

        # Model architecture
        self.model = nn.Sequential(
            nn.Linear(n_features, 512),
            nn.Dropout(0.5),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(512, 256),
            nn.Dropout(0.5),
            nn.LeakyReLU(0.2, inplace=True),
            nn.Linear(256, 1),
        )
        self.output_sig = nn.Sigmoid()
        self.loss = loss()

        # Hyperparameters
        self.params = {
            "lr": lr,
            "n_features": n_features,
        }

        # Extra configuration
        self.progress_bar = None

    def forward(self, input_1, input_2):
        s1 = self.model(input_1)
        s2 = self.model(input_2)

        return self.output_sig(s1 - s2)

    def predict(self, input):
        return self.model(input)

    def configure_optimizers(self):
        return Adam(self.parameters(), lr=self.params["lr"])

    def on_train_start(self):
        self.progress_bar = tqdm(
            total=5000,
            desc="Processing",
            unit="iteration",
        )

        if self.logger:
            self.logger.log_hyperparams(self.params)

    def on_train_epoch_end(self) -> None:
        self.progress_bar.update(1)

    def training_step(self, batch, batch_idx):
        input_1, input_2, target = batch
        output = self.forward(input_1, input_2)
        loss = self.loss(output, target)

        self.log_dict(
            {"train_loss": loss},
        )

        return loss
