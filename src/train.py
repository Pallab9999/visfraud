from __future__ import annotations

import numpy as np
import torch
from collections import Counter
from imblearn.over_sampling import SMOTE
from sklearn.metrics import (auc, average_precision_score, confusion_matrix,
                             f1_score, precision_score, recall_score, roc_auc_score)
from torch.utils.data import DataLoader

from .dataset import TransactionImageDataset


def seed_everything(seed: int = 42):
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def get_class_weights(labels: np.ndarray) -> torch.Tensor:
    counts = Counter(labels.tolist())
    total = len(labels)
    weights = [total / counts[i] if counts[i] > 0 else 0.0 for i in sorted(counts)]
    return torch.tensor(weights, dtype=torch.float32)


def oversample_images(images: np.ndarray, labels: np.ndarray, random_state: int = 0):
    n_samples, height, width = images.shape
    flattened = images.reshape(n_samples, -1)
    smote = SMOTE(random_state=random_state)
    x_resampled, y_resampled = smote.fit_resample(flattened, labels)
    x_resampled = x_resampled.reshape(-1, height, width)
    return x_resampled.astype(np.float32), y_resampled.astype(np.int64)


def create_dataloader(dataset: TransactionImageDataset, batch_size: int = 64, shuffle: bool = True, num_workers: int = 0):
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)


def evaluate_model(model: torch.nn.Module, dataloader: DataLoader, device: torch.device):
    model.eval()
    all_preds = []
    all_probs = []
    all_labels = []
    softmax = torch.nn.Softmax(dim=1)
    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            probabilities = softmax(outputs)[:, 1]
            preds = torch.argmax(outputs, dim=1)
            all_preds.extend(preds.cpu().numpy())
            all_probs.extend(probabilities.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
    all_labels = np.array(all_labels)
    all_preds = np.array(all_preds)
    all_probs = np.array(all_probs)
    metrics = {
        "f1": f1_score(all_labels, all_preds, zero_division=0),
        "precision": precision_score(all_labels, all_preds, zero_division=0),
        "recall": recall_score(all_labels, all_preds, zero_division=0),
        "roc_auc": roc_auc_score(all_labels, all_probs),
        "pr_auc": average_precision_score(all_labels, all_probs),
        "confusion_matrix": confusion_matrix(all_labels, all_preds).tolist(),
    }
    return metrics


def train_epoch(model: torch.nn.Module, dataloader: DataLoader, criterion, optimizer, device: torch.device):
    model.train()
    running_loss = 0.0
    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * inputs.size(0)
    return running_loss / len(dataloader.dataset)


def train_model(model: torch.nn.Module,
                train_dataset: TransactionImageDataset,
                val_dataset: TransactionImageDataset,
                device: torch.device,
                batch_size: int = 64,
                lr: float = 1e-3,
                num_epochs: int = 20):
    train_loader = create_dataloader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = create_dataloader(val_dataset, batch_size=batch_size, shuffle=False)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    labels = np.array([int(y) for _, y in train_dataset])
    class_weights = get_class_weights(labels).to(device)
    criterion = torch.nn.CrossEntropyLoss(weight=class_weights)

    history = {"train_loss": [], "val_f1": [], "val_roc_auc": [], "val_pr_auc": []}
    for epoch in range(1, num_epochs + 1):
        loss = train_epoch(model, train_loader, criterion, optimizer, device)
        metrics = evaluate_model(model, val_loader, device)
        history["train_loss"].append(loss)
        history["val_f1"].append(metrics["f1"])
        history["val_roc_auc"].append(metrics["roc_auc"])
        history["val_pr_auc"].append(metrics["pr_auc"])
        print(f"Epoch {epoch}/{num_epochs}: loss={loss:.4f}, f1={metrics['f1']:.4f}, roc_auc={metrics['roc_auc']:.4f}, pr_auc={metrics['pr_auc']:.4f}")
    return model, history


def save_checkpoint(model: torch.nn.Module, path: str):
    torch.save(model.state_dict(), path)


def load_checkpoint(model: torch.nn.Module, path: str, device: torch.device):
    model.load_state_dict(torch.load(path, map_location=device))
    model.to(device)
    model.eval()
    return model
