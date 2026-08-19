# E-commerce Analytics & Churn Prediction

This repository is a structured pet project for building an end-to-end e-commerce analytics platform in Python. The goal is to go from raw transactional data to business insights, customer analytics, and a churn prediction model.

The project is designed as a learning and portfolio-focused pipeline that combines:

- data engineering and ingestion
- schema validation with Pydantic
- data preprocessing and feature engineering
- sales and customer analytics
- machine learning for customer churn prediction
- REST API exposure with FastAPI

## Why this project?

This project is useful because it reflects a realistic product analytics workflow:

- raw data arrives in CSV/Excel format
- data is validated and normalized
- business metrics are computed
- customer behavior is analyzed
- churn risk is predicted from historical patterns
- results can be exposed through a simple API

It is a strong example of a Python + Data Science project that demonstrates both analytical thinking and software engineering skills.

## Tech stack

- Python 3.11+
- pandas
- NumPy
- scikit-learn
- Pydantic
- FastAPI
- pytest
- Jupyter (for analysis and exploration)

## Project roadmap

### Stage 1 — Foundation
- [x] Initialize repository structure
- [x] Add environment configuration
- [x] Set up dependencies and project documentation
- [x] Create the dataset loader

### Stage 2 — Data quality and validation
- [x] Define transaction schema and column mapping
- [x] Validate input records with Pydantic
- [ ] Clean missing values and invalid records
- [ ] Normalize dates, numeric fields, and text values

### Stage 3 — Analytics
- [x] Perform initial exploratory data analysis
- [ ] Calculate revenue, orders, and average order value as reusable analytics functions
- [ ] Build retention and cohort analysis
- [ ] Perform customer segmentation and RFM analysis

### Stage 4 — Machine learning
- [ ] Build a churn prediction dataset
- [ ] Train a baseline classifier
- [ ] Evaluate model performance
- [ ] Interpret feature importance

### Stage 5 — API and deployment
- [ ] Expose analytics via FastAPI
- [ ] Add health and prediction endpoints
- [ ] Add tests for core workflows
- [ ] Dockerize the project

## Project structure

```text
.
├── data/
│   ├── raw/
│   └── processed/
├── scripts/
│   └── download_dataset.py
├── notebooks/
│   └── dataset.ipynb
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data/
│   │   ├── __init__.py
│   │   ├── loader.py
│   │   └── schema.py
│   ├── analytics/
│   ├── ml/
│   └── api/
├── tests/
│   ├── test_data_loader.py
│   └── test_transaction_schema.py
├── .gitignore
├── README.md
├── requirements.txt
├── download.ps1
├── download.sh
└── pytest.ini
```

## Dataset

This project uses the [Online Retail II dataset](https://archive.ics.uci.edu/dataset/502/online%2Bretail%2Bii) from the UCI Machine Learning Repository.

The raw dataset includes columns such as:

```text
Invoice, StockCode, Description, Quantity, InvoiceDate, Price, Customer ID, Country
```

Inside the project, these are normalized to a cleaner structure:

```text
invoice_no, stock_code, description, quantity, invoice_date, unit_price, customer_id, country
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd ecommerce-analytics
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

This installs the required libraries for data processing, validation, and tests, including `pandas`, `numpy`, `openpyxl`, `pydantic`, and `pytest`.

## Download the dataset

This project uses the [Online Retail II dataset](https://archive.ics.uci.edu/dataset/502/online%2Bretail%2Bii) from the UCI Machine Learning Repository.

The dataset is not stored in the repository itself, so you need to download it before working with the project.

### Recommended: use the platform helper script

Windows PowerShell:

```powershell
.\download.ps1
```

macOS / Linux:

```bash
bash download.sh
```

### Alternative: run the Python downloader directly

Windows PowerShell:

```powershell
python scripts\download_dataset.py
```

macOS / Linux:

```bash
python scripts/download_dataset.py
```

### Expected output location

The script downloads the dataset into:

```text
data/raw/online_retail_II.xlsx
```

The archive is also stored temporarily in:

```text
data/raw/online_retail_ii.zip
```

> The dataset is large and is intended to be downloaded locally. It is not committed to GitHub.

## Working with the dataset

The project expects the raw dataset to be loaded from `data/raw/online_retail_II.xlsx` and then normalized to the internal schema used by the project.

### Example: load transactions

```python
from pathlib import Path
from src.data.loader import load_transactions

file_path = Path("data/raw/online_retail_II.xlsx")
transactions = load_transactions(file_path)

print(transactions.head())
print(transactions.columns.tolist())
```

The loader automatically:

- reads the Excel file
- maps raw column names to project names
- validates that required columns are present
- returns a pandas DataFrame with the normalized schema

Expected normalized columns:

```text
invoice_no, stock_code, description, quantity, invoice_date, unit_price, customer_id, country
```

### Example: inspect the loaded data

```python
print(transactions.shape)
print(transactions["invoice_no"].head())
print(transactions["country"].value_counts().head())
```

## Exploratory data analysis

The first EDA stage is available in [notebooks/dataset.ipynb](notebooks/dataset.ipynb). It loads the downloaded workbook through the project loader and checks:

- dataset size, date range, and unique invoices, products, and customers;
- missing customer IDs, missing descriptions, duplicates, returns, and zero-price rows;
- gross revenue, return value, net revenue, sales lines, and return lines;
- monthly revenue, order count, customer count, and average order value;
- revenue concentration by country and product.

The current dataset contains `1,067,371` rows covering December 2009 to December 2011. Customer IDs are missing in `22.77%` of rows, while negative quantities represent return transactions and should remain identifiable during preprocessing.

To open the notebook in VS Code or Jupyter, first download the dataset and then run the cells from top to bottom:

```bash
jupyter notebook notebooks/dataset.ipynb
```

The notebook is exploratory; reusable cleaning and analytics logic will be moved into `src/` modules in the following stages.

## Run tests

```bash
python -m pytest
```

This verifies the basic data loading behavior and schema checks that are already implemented in the project.

## Notes

This repository is intentionally built as a step-by-step project. The idea is to implement one part of the pipeline at a time, commit the progress, and keep the history readable and meaningful for GitHub.

The long-term goal is to evolve this project into a complete analytics + ML workflow, but the first milestone is to build a clean and understandable foundation.
