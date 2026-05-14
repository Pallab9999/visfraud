# VisFraud: Visual Saliency for Fraud Pattern Detection

This project explores whether visual representations of financial transactions can make fraud patterns *perceptible* — to both neural networks and human analysts. Inspired by anomaly detection techniques in astrophysical imaging (where rare structured signals must be found in high-dimensional visual noise), we encode transaction data as images and use Grad-CAM saliency maps to reveal what "fraud looks like" visually.

## What this project does

- Converts credit card transaction records into visual encodings using Gramian Angular Fields (GAF), Recurrence Plots (RP), and feature heatmaps.
- Trains a compact PyTorch CNN to classify legitimate vs fraudulent transactions from these images.
- Applies Grad-CAM explainability to overlay saliency heatmaps on encoded images, highlighting the regions the model uses for fraud decisions.
- Compares image-based fraud detection to a tabular benchmark using XGBoost-style metrics.

## Repository structure

```
visfraud/
├── data/
│   └── creditcard.csv          # download from Kaggle (gitignored)
├── notebooks/
│   ├── 01_encoding.ipynb       # Data → Image encoding + visualisation
│   ├── 02_training.ipynb       # CNN training + evaluation
│   └── 03_gradcam.ipynb        # Grad-CAM + analysis
├── outputs/
│   ├── figures/                # Saved plots
│   └── models/                 # Saved model checkpoints
├── src/
│   ├── encode.py               # GAF, RP, heatmap functions
│   ├── dataset.py              # PyTorch Dataset class
│   ├── model.py                # CNN architecture
│   ├── train.py                # Training loop
│   └── gradcam_utils.py        # Grad-CAM wrapper
├── requirements.txt
└── README.md
```

## Installation

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

1. Download `creditcard.csv` from Kaggle and place it in `data/`
2. Run the notebooks in order:
   - `notebooks/01_encoding.ipynb`
   - `notebooks/02_training.ipynb`
   - `notebooks/03_gradcam.ipynb`

## Notes

- The dataset is highly imbalanced, so training uses weighted loss and SMOTE oversampling.
- Grad-CAM visualizations are generated for fraud predictions to make the model's reasoning interpretable.
- The astrophysics-inspired framing is intentionally preserved: we treat fraud detection as a structured signal-finding problem in noisy, high-dimensional images.
