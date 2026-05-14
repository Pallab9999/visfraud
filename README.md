# VisFraud: Visual Saliency for Fraud Pattern Detection

[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-ee4c2c.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-active-success.svg)]()

> **Visual fraud detection through image encoding and interpretable deep learning**

## 🎯 Overview

VisFraud explores whether visual representations of financial transactions can make fraud patterns *perceptible* — to both neural networks and human analysts. Inspired by anomaly detection techniques in astrophysical imaging (where rare structured signals must be found in high-dimensional visual noise), we encode transaction data as images and use Grad-CAM saliency maps to reveal what "fraud looks like" visually.

### Key Features

✨ **Visual Encoding**: Converts credit card transactions into visual representations using:
- **Gramian Angular Fields (GAF)** — Captures temporal correlations in polar space
- **Recurrence Plots (RP)** — Visualizes self-similarity and pattern structure
- **Feature Heatmaps** — Direct intensity-based feature mapping

🧠 **Deep Learning Classification**: Lightweight CNN (14K parameters) optimized for GPU acceleration

🔍 **Interpretability**: Grad-CAM saliency maps highlight fraud-discriminative regions in images

📊 **Benchmarking**: Comparative evaluation against XGBoost tabular baseline

## 📂 Repository Structure

```
visfraud/
├── data/                           # Dataset directory
│   └── creditcard.csv              # Kaggle Credit Card Fraud Detection (gitignored)
├── notebooks/                      # Jupyter notebooks for analysis
│   ├── 01_encoding.ipynb          # Data → Image encoding + visualization
│   ├── 02_training.ipynb          # CNN + XGBoost training & evaluation
│   └── 03_gradcam.ipynb           # Grad-CAM saliency analysis
├── outputs/                        # Generated artifacts
│   ├── figures/                    # Saved plots and visualizations
│   └── models/                     # Trained model checkpoints
├── scripts/
│   └── download_data.py            # Kaggle dataset downloader
├── src/                            # Core source code
│   ├── encode.py                   # GAF, RP, heatmap encoding functions
│   ├── dataset.py                  # PyTorch Dataset class
│   ├── model.py                    # FraudCNN architecture
│   ├── train.py                    # Training pipeline
│   └── gradcam_utils.py            # Grad-CAM visualization wrapper
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── REPORT.md                       # Detailed project report
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip or conda
- CUDA (optional, for GPU acceleration)
- Kaggle account (for dataset download)

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/visfraud.git
cd visfraud
```

**2. Create and activate virtual environment:**
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

> ⚠️ **Note**: The Grad-CAM dependency is installed from GitHub source because `pytorch-grad-cam` is not available on PyPI for some Python 3.13+ environments.

### Download Dataset

**Option A: Manual Download**
1. Download `creditcard.csv` from [Kaggle](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
2. Place it in the `data/` directory

**Option B: Automated Download**
```bash
# Configure Kaggle credentials (one-time setup)
# See: https://github.com/Kaggle/kaggle-api#api-credentials
python scripts/download_data.py
```

## 📖 Usage

Run the notebooks in sequence to reproduce the full analysis:

```bash
jupyter lab notebooks/
```

Or use VS Code with Jupyter extension:
- `notebooks/01_encoding.ipynb` — Data loading, encoding, visualization
- `notebooks/02_training.ipynb` — Model training, evaluation, XGBoost comparison
- `notebooks/03_gradcam.ipynb` — Saliency map generation and interpretation

## 🔬 Technical Details

### Dataset
- **Source**: Kaggle Credit Card Fraud Detection
- **Size**: 284,807 transactions across 31 features
- **Class Distribution**: Highly imbalanced (0.172% fraud rate)
- **Encoding Output**: 28×28 images (GAF, RP) or heatmaps

### Model Architecture
```
FraudCNN
├── Conv2d(3 → 32, kernel=3) + ReLU + MaxPool(2,2)
├── Conv2d(32 → 64, kernel=3) + ReLU + MaxPool(2,2)
├── Conv2d(64 → 128, kernel=3) + ReLU + AdaptiveAvgPool
└── Linear(128 → 2 classes)
Total Parameters: ~14K
```

### Handling Imbalanced Data
- **Weighted Cross-Entropy Loss** — Penalizes minority class misclassification
- **SMOTE Oversampling** — Generates synthetic fraud samples during training
- **Class Weighting** — Ratio: `(legitimate_count / fraud_count)`

### Explainability
Grad-CAM produces visual explanations by:
1. Computing gradient of fraud class with respect to final conv layer
2. Scaling by activation maps to highlight important regions
3. Overlaying heatmaps on original encoded images for analyst review

## 📊 Results & Performance

See [REPORT.md](REPORT.md) for:
- Detailed performance metrics (ROC-AUC, PR-AUC, F1-scores)
- Training curves and convergence analysis
- Grad-CAM interpretation examples
- Comparative analysis vs. XGBoost baseline

## 🛠️ Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| torch | 2.0+ | Deep learning framework |
| torchvision | 0.15+ | Computer vision utilities |
| scikit-learn | 1.2+ | ML metrics & SMOTE |
| pandas | 1.5+ | Data manipulation |
| numpy | 1.23+ | Numerical computing |
| matplotlib | 3.7+ | Visualization |
| seaborn | 0.12+ | Statistical plots |
| pyts | 0.2+ | Time series to image encoding |
| xgboost | 1.7+ | Gradient boosting benchmark |
| kaggle | 1.5+ | Dataset download CLI |
| grad-cam | Latest | Saliency map generation |

## 📝 License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

## 🤝 Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### How to Contribute
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -am 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

## 📮 Citation

If you use VisFraud in your research, please cite:

```bibtex
@software{visfraud2026,
  title={VisFraud: Visual Saliency for Fraud Pattern Detection},
  author={Your Name},
  year={2026},
  url={https://github.com/your-username/visfraud}
}
```

## 🙏 Acknowledgments

- **Dataset**: Kaggle Credit Card Fraud Detection by MLG-ULB
- **Grad-CAM**: [pytorch-grad-cam](https://github.com/jacobgil/pytorch-grad-cam)
- **Inspiration**: Astrophysical anomaly detection techniques
- **Community**: PyTorch, scikit-learn, and open-source ML communities

## ❓ FAQ

**Q: Why encode transactions as images?**  
A: Images enable visual pattern recognition and leverage powerful CNN architectures. Treating fraud detection as a signal-finding problem in "noisy images" provides novel interpretability.

**Q: Why Grad-CAM?**  
A: Grad-CAM shows *which parts* of the encoded image drive fraud predictions, making the model's decision process transparent to analysts.

**Q: Can I use a pre-trained model?**  
A: The project includes pre-trained weights in `outputs/models/`. Load using `torch.load()` in your pipeline.

**Q: Is GPU required?**  
A: No, but highly recommended. The model auto-detects CUDA and falls back to CPU if unavailable.

## 📞 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/your-username/visfraud/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/visfraud/discussions)
- **Email**: your-email@example.com

---

**Last Updated**: May 14, 2026 | **Status**: ✅ Active & Maintained
