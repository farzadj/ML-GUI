# ML-GUI

A PyQt5-based GUI for building and training simple machine learning models.

## Prerequisites

- **Python**: version 3.8 or higher is recommended.
- **Dependencies**:
  - PyQt5
  - pandas
  - numpy
  - matplotlib
  - seaborn
  - scikit-learn
  - tensorflow
  - joblib (optional for model export)

Install the requirements with pip:

```bash
pip install PyQt5 pandas numpy matplotlib seaborn scikit-learn tensorflow joblib
```

## Getting Started

Run the application from the repository root:

```bash
python ML-GUI.py
```

This launches the main window from which you can load datasets and start training.

## Features

- **Load CSV files**: inspect data in a table and visualize columns.
- **Train models**: create training and test sets and fit TensorFlow models directly from the GUI.
- **Expert window**: access advanced options like grid search, cross validation, and data scaling.

