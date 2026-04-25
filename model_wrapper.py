import torch
import torch.nn as nn
import torch.nn.functional as F

class ECGModel(nn.Module):
    """
    CNN-BiLSTM-Attention architecture matching dheerajthuvara/ecg-arrhythmia-detection.
    Keys extracted from best_model.pt state_dict.
    """
    def __init__(self, config):
        super(ECGModel, self).__init__()
        
        filters = config.get("cnn_filters", [32, 64, 128])
        ks = config.get("kernel_size", 5)
        lstm_hidden = config.get("lstm_hidden", 128)
        lstm_layers = config.get("lstm_layers", 2)
        dropout = config.get("dropout", 0.3)
        num_classes = config.get("num_classes", 5)
        
        # CNN Sequential
        self.cnn = nn.Sequential(
            # Block 1
            nn.Conv1d(1, filters[0], ks, padding="same"),
            nn.BatchNorm1d(filters[0]),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Dropout(dropout),
            # Block 2
            nn.Conv1d(filters[0], filters[1], ks, padding="same"),
            nn.BatchNorm1d(filters[1]),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Dropout(dropout),
            # Block 3
            nn.Conv1d(filters[1], filters[2], ks, padding="same"),
            nn.BatchNorm1d(filters[2]),
            nn.ReLU(),
            nn.MaxPool1d(2),
            nn.Dropout(dropout)
        )
        
        # BiLSTM
        self.bilstm = nn.LSTM(
            input_size=filters[2],
            hidden_size=lstm_hidden,
            num_layers=lstm_layers,
            batch_first=True,
            bidirectional=True,
            dropout=dropout if lstm_layers > 1 else 0
        )
        
        # Attention Layer
        # Based on keys 'attention.weight' and 'attention.bias'
        # This is likely a self-attention mechanism or a simple linear attention
        self.attention = nn.Linear(lstm_hidden * 2, 1)
        
        # Classifier Sequential
        self.classifier = nn.Sequential(
            nn.Linear(lstm_hidden * 2, 64),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        # x: (batch, 1, 180)
        x = self.cnn(x)
        
        # (batch, channels, seq) -> (batch, seq, channels)
        x = x.permute(0, 2, 1)
        
        # lstm_out: (batch, seq, 2 * hidden)
        lstm_out, _ = self.bilstm(x)
        
        # Attention mechanism
        # att_weights: (batch, seq, 1)
        att_weights = torch.tanh(self.attention(lstm_out))
        att_weights = F.softmax(att_weights, dim=1)
        
        # context_vector: (batch, 2 * hidden)
        context_vector = torch.sum(att_weights * lstm_out, dim=1)
        
        # classifier
        out = self.classifier(context_vector)
        return out
