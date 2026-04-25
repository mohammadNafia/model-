import torch
import torch.nn as nn


class ECGModel(nn.Module):
    """
    CNN-BiLSTM fallback wrapper for dheerajthuvara/ecg-arrhythmia-detection.

    Architecture is reverse-engineered from models/model_config.json:
        cnn_filters : [32, 64, 128]
        kernel_size : 5
        lstm_hidden : 128
        lstm_layers : 2
        dropout     : 0.3
        num_classes : 5
    """

    def __init__(self, config: dict):
        super().__init__()

        filters      = config.get("cnn_filters",  [32, 64, 128])
        ks           = config.get("kernel_size",  5)
        lstm_hidden  = config.get("lstm_hidden",  128)
        lstm_layers  = config.get("lstm_layers",  2)
        dropout      = config.get("dropout",      0.3)
        num_classes  = config.get("num_classes",  5)

        # --- Block 1 ---
        self.conv1    = nn.Conv1d(1,         filters[0], ks, padding="same")
        self.bn1      = nn.BatchNorm1d(filters[0])
        self.relu1    = nn.ReLU()
        self.pool1    = nn.MaxPool1d(2)
        self.drop1    = nn.Dropout(dropout)

        # --- Block 2 ---
        self.conv2    = nn.Conv1d(filters[0], filters[1], ks, padding="same")
        self.bn2      = nn.BatchNorm1d(filters[1])
        self.relu2    = nn.ReLU()
        self.pool2    = nn.MaxPool1d(2)
        self.drop2    = nn.Dropout(dropout)

        # --- Block 3 ---
        self.conv3    = nn.Conv1d(filters[1], filters[2], ks, padding="same")
        self.bn3      = nn.BatchNorm1d(filters[2])
        self.relu3    = nn.ReLU()
        self.pool3    = nn.MaxPool1d(2)
        self.drop3    = nn.Dropout(dropout)

        # --- BiLSTM ---
        self.lstm = nn.LSTM(
            input_size   = filters[2],
            hidden_size  = lstm_hidden,
            num_layers   = lstm_layers,
            batch_first  = True,
            bidirectional= True,
            dropout      = dropout if lstm_layers > 1 else 0.0,
        )

        # --- Classifier ---
        self.fc = nn.Linear(lstm_hidden * 2, num_classes)

    def forward(self, x):
        # x : (batch, 1, seq_len)
        x = self.drop1(self.pool1(self.relu1(self.bn1(self.conv1(x)))))
        x = self.drop2(self.pool2(self.relu2(self.bn2(self.conv2(x)))))
        x = self.drop3(self.pool3(self.relu3(self.bn3(self.conv3(x)))))

        # (batch, channels, reduced_len) → (batch, reduced_len, channels)
        x = x.permute(0, 2, 1)

        lstm_out, _ = self.lstm(x)

        # Take last time-step output
        last = lstm_out[:, -1, :]
        return self.fc(last)
