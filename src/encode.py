import numpy as np
import pandas as pd
from pyts.image import GramianAngularField, RecurrencePlot


def _normalize_series(series: np.ndarray, target_range=(-1.0, 1.0)) -> np.ndarray:
    min_val = np.nanmin(series)
    max_val = np.nanmax(series)
    if max_val == min_val:
        return np.full_like(series, target_range[0])
    scaled = (series - min_val) / (max_val - min_val)
    lower, upper = target_range
    return scaled * (upper - lower) + lower


def _prepare_features(df: pd.DataFrame, feature_cols=None):
    if feature_cols is None:
        feature_cols = [f"V{i}" for i in range(1, 29)]
        if "Amount" in df.columns:
            feature_cols.append("Amount")
        if "Time" in df.columns:
            feature_cols.append("Time")
    missing = [c for c in feature_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")
    features = df[feature_cols].astype(float).fillna(0.0)
    return features


def encode_gaf(df: pd.DataFrame, image_size: int = 28, feature_cols=None) -> np.ndarray:
    features = _prepare_features(df, feature_cols)
    values = features.to_numpy(dtype=float)
    normalized = np.apply_along_axis(_normalize_series, 1, values)
    gaf = GramianAngularField(image_size=image_size, method="summation")
    images = gaf.fit_transform(normalized)
    return images.astype(np.float32)


def _resize_image(image: np.ndarray, target_size: int = 28) -> np.ndarray:
    y_repeat = int(np.ceil(target_size / image.shape[0]))
    x_repeat = int(np.ceil(target_size / image.shape[1]))
    scaled = np.repeat(np.repeat(image, y_repeat, axis=0), x_repeat, axis=1)
    return scaled[:target_size, :target_size]


def encode_rp(df: pd.DataFrame, image_size: int = 28, feature_cols=None) -> np.ndarray:
    features = _prepare_features(df, feature_cols)
    values = features.to_numpy(dtype=float)
    normalized = np.apply_along_axis(_normalize_series, 1, values)
    rp = RecurrencePlot(dimension=1, time_delay=1, threshold="point", percentage=20)
    images = rp.fit_transform(normalized)
    if images.shape[1] != image_size or images.shape[2] != image_size:
        images = np.array([_resize_image(img, target_size=image_size) for img in images], dtype=np.float32)
    return images.astype(np.float32)


def _scale_heatmap(image: np.ndarray, target_size: int = 28) -> np.ndarray:
    y_repeat = int(np.ceil(target_size / image.shape[0]))
    x_repeat = int(np.ceil(target_size / image.shape[1]))
    scaled = np.repeat(np.repeat(image, y_repeat, axis=0), x_repeat, axis=1)
    cropped = scaled[:target_size, :target_size]
    return cropped


def encode_heatmap(df: pd.DataFrame, grid_shape=(5, 6), target_size=28, feature_cols=None) -> np.ndarray:
    features = _prepare_features(df, feature_cols)
    values = features.to_numpy(dtype=float)
    num_features = grid_shape[0] * grid_shape[1]
    if values.shape[1] < num_features:
        padded = np.zeros((values.shape[0], num_features), dtype=float)
        padded[:, : values.shape[1]] = values
        values = padded
    elif values.shape[1] > num_features:
        values = values[:, :num_features]
    images = values.reshape((-1, grid_shape[0], grid_shape[1]))
    images = np.array([_scale_heatmap(img, target_size=target_size) for img in images], dtype=np.float32)
    images = np.nan_to_num(images)
    return images


def save_image_dataset(images: np.ndarray, labels: np.ndarray, output_path: str) -> None:
    np.savez_compressed(output_path, images=images, labels=labels)


def load_image_dataset(npz_path: str):
    data = np.load(npz_path)
    return data["images"], data["labels"]
