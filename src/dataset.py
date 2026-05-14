from __future__ import annotations

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset

from .encode import encode_gaf, encode_heatmap, encode_rp


class TransactionImageDataset(Dataset):
    def __init__(self, images: np.ndarray, labels: np.ndarray, transform=None):
        self.images = images.astype(np.float32)
        self.labels = labels.astype(np.int64)
        self.transform = transform

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = torch.tensor(int(self.labels[idx]), dtype=torch.long)
        if self.transform is not None:
            image = self.transform(image)
        else:
            image = torch.from_numpy(image).unsqueeze(0)
        return image, label

    @classmethod
    def from_numpy(cls, npz_path: str, transform=None):
        dataset = np.load(npz_path)
        images = dataset["images"]
        labels = dataset["labels"]
        return cls(images, labels, transform=transform)

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame, encoding: str = "gaf", image_size: int = 28, transform=None):
        label_col = "Class" if "Class" in df.columns else "label"
        labels = df[label_col].to_numpy(dtype=int)
        if encoding == "gaf":
            images = encode_gaf(df, image_size=image_size)
        elif encoding == "rp":
            images = encode_rp(df, image_size=image_size)
        elif encoding == "heatmap":
            images = encode_heatmap(df, target_size=image_size)
        else:
            raise ValueError(f"Unsupported encoding: {encoding}")
        return cls(images, labels, transform=transform)
