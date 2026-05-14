# Contributing to VisFraud

Thank you for your interest in contributing to VisFraud! This document provides guidelines and instructions for contributing to the project.

## 🎯 Code of Conduct

Please note that this project is released with a [Contributor Code of Conduct](CODE_OF_CONDUCT.md). By participating in this project you agree to abide by its terms.

## 💡 Ways to Contribute

### Bug Reports
- **Found a bug?** Please [open an issue](../../issues) with:
  - Clear, descriptive title
  - Step-by-step reproduction instructions
  - Expected vs actual behavior
  - Python version, PyTorch version, OS
  - Relevant error logs or stack traces

### Feature Requests
- Suggest new encoding methods (beyond GAF/RP)
- Propose alternative model architectures
- Suggest new explainability techniques
- Propose performance optimizations

### Documentation
- Improve existing documentation
- Add examples or tutorials
- Fix typos or clarify unclear sections
- Create notebooks demonstrating new features

### Code Contributions
- Bug fixes
- Performance improvements
- New encoding functions
- Additional evaluation metrics
- Extended test coverage

## 🔧 Development Setup

### 1. Fork and Clone
```bash
git clone https://github.com/your-username/visfraud.git
cd visfraud
```

### 2. Create Development Branch
```bash
git checkout -b feature/your-feature-name
```

### 3. Set Up Development Environment
```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 4. Install Development Dependencies (Optional)
```bash
pip install pytest black pylint jupyter
```

## 📋 Development Workflow

### Before Starting
1. Check [issues](../../issues) for duplicate/related work
2. Create an issue to discuss your proposed changes
3. Get feedback before investing significant effort

### Code Standards

#### Style Guide
- Follow PEP 8 conventions
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular

#### Example Function Documentation
```python
def encode_gaf(data: np.ndarray, image_size: int = 28) -> np.ndarray:
    """
    Encode time series data using Gramian Angular Field.

    Parameters
    ----------
    data : np.ndarray
        Input time series data (1D array).
    image_size : int, default=28
        Output image dimensions (image_size x image_size).

    Returns
    -------
    np.ndarray
        Encoded GAF image (image_size x image_size).

    References
    ----------
    Wang, Z., & Oates, T. (2015). Imaging Time-Series to Improve
    Classification and Imputation. IJCAI.
    """
```

#### Formatting with Black
```bash
black src/ notebooks/
```

#### Linting with Pylint
```bash
pylint src/
```

### Testing

#### Run Tests
```bash
pytest tests/
```

#### Add Tests
- Create test file: `tests/test_[module].py`
- Use descriptive test names: `test_[function]_[scenario]`
- Aim for >80% code coverage

Example test:
```python
import pytest
import numpy as np
from src.encode import encode_gaf

def test_encode_gaf_output_shape():
    """Test that GAF encoding produces correct image dimensions."""
    data = np.random.randn(100)
    image = encode_gaf(data, image_size=28)
    assert image.shape == (28, 28)

def test_encode_gaf_value_range():
    """Test that GAF values are normalized to [0, 1]."""
    data = np.random.randn(100)
    image = encode_gaf(data, image_size=28)
    assert np.min(image) >= 0.0
    assert np.max(image) <= 1.0
```

## 📝 Commit Guidelines

### Commit Messages
- Use imperative mood: "Add feature" not "Added feature"
- Start with a verb: Add, Fix, Update, Refactor, Optimize
- Keep first line < 50 characters
- Add detailed explanation after blank line if needed

Examples:
```
Add GAF encoding function with docstring

Fix SMOTE oversampling for imbalanced batches
Update Grad-CAM visualization to support batch processing

Refactor model architecture for better GPU memory efficiency
```

### Commit Frequency
- Commit logical, atomic changes
- Avoid mixing refactoring with feature additions
- Each commit should be independently understandable

## 🔄 Pull Request Process

### Before Creating PR
1. Update your fork's main branch
2. Rebase your feature branch on main
3. Run tests locally and verify they pass
4. Update documentation and README if needed

### PR Template
```markdown
## Description
Brief summary of changes.

## Related Issue
Fixes #[issue_number]

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement

## Testing
How was this tested? Include relevant test output.

## Checklist
- [ ] Code follows project style guide
- [ ] Docstrings added/updated
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No new warnings introduced
```

### PR Review Process
- Address feedback promptly
- Respond to comments with explanations or fixes
- Request re-review after making changes
- Be respectful and constructive in discussions

## 📚 Project Structure Notes

### `src/` Module Organization
- `encode.py` — All encoding functions (GAF, RP, heatmap)
- `dataset.py` — PyTorch Dataset class
- `model.py` — Neural network architectures
- `train.py` — Training pipeline and utilities
- `gradcam_utils.py` — Saliency visualization

### Notebook Conventions
- Notebooks are for exploration and demonstration
- Keep them reproducible and well-commented
- Clear section headers with `# ===== Section Title =====`
- Add markdown explanations between code cells

## 🐛 Debugging Tips

### Common Issues

**ImportError: No module named 'grad_cam'**
```bash
pip install git+https://github.com/jacobgil/pytorch-grad-cam.git#egg=grad-cam
```

**CUDA Out of Memory**
- Reduce batch size in training
- Use smaller image size (e.g., 16x16 instead of 28x28)
- Check GPU memory: `nvidia-smi`

**Kaggle API Errors**
- Verify credentials in `~/.kaggle/kaggle.json`
- Ensure file permissions: `chmod 600 ~/.kaggle/kaggle.json` (Unix/macOS)

### Logging
```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
```

## 📖 Documentation Standards

### Docstring Format
Use NumPy-style docstrings:

```python
def my_function(param1: int, param2: str) -> bool:
    """
    Brief one-line description.

    Longer description explaining purpose, behavior, and edge cases.

    Parameters
    ----------
    param1 : int
        Description of param1.
    param2 : str
        Description of param2.

    Returns
    -------
    bool
        Description of return value.

    Raises
    ------
    ValueError
        When parameters are invalid.

    Examples
    --------
    >>> result = my_function(42, "test")
    >>> print(result)
    True
    """
```

### README Updates
- Keep README current with new features
- Add examples for new encoding methods
- Update dependencies if added/changed
- Add new troubleshooting sections as issues arise

## 🎓 Learning Resources

### Time Series to Image Encoding
- Wang, Z., & Oates, T. (2015). Imaging Time-Series to Improve Classification and Imputation
- Recurrence Plot theory: http://www.recurrence-plot.tk/

### Grad-CAM
- Selvaraju et al. (2016). Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization
- Implementation: https://github.com/jacobgil/pytorch-grad-cam

### PyTorch Best Practices
- Official PyTorch tutorials: https://pytorch.org/tutorials/
- PyTorch Lightning for simplified training: https://lightning.ai/

## 🚀 Recognition

Contributors will be recognized in:
- [CONTRIBUTORS.md](CONTRIBUTORS.md)
- GitHub contributors page
- Project releases

## ❓ Questions?

- **Issues & Bugs**: [GitHub Issues](../../issues)
- **Discussions**: [GitHub Discussions](../../discussions)
- **Email**: your-email@example.com

---

Thank you for contributing to VisFraud! 🙏
