# E-commerce Analytics & ML Platform

End-to-end analytics platform for an online store: from raw transactional CSV files to clean datasets, sales analytics, customer segmentation, churn prediction, and an analytical FastAPI service.

## Development Roadmap

- [x] **01 - Initialize project**: Basic repository structure, configuration, dependencies, and README.
- [ ] **02 - Data loading & schema definition**: Load and parse input CSV files.
- [ ] **03 - Data validation**: Validate transaction schemas with Pydantic.
- [ ] **04 - Preprocessing pipeline**: Clean data, handle missing values, and detect anomalies.
- [ ] **05 - Sales analytics engine**: Calculate revenue, average order value, and order dynamics.
- [ ] **06 - Customer analytics**: Add RFM segmentation, cohort analysis, and retention metrics.
- [ ] **07 - PostgreSQL storage**: Store transactions and analytical aggregates in a database.
- [ ] **08 - ETL pipeline**: Automate data extraction, transformation, and loading.
- [ ] **09 - Exploratory Data Analysis**: Add visual exploration and business insights.
- [ ] **10 - Churn prediction model**: Train a machine learning model to estimate customer churn risk.
- [ ] **11 - Model evaluation & metrics**: Evaluate model quality with ROC-AUC, precision, recall, and feature interpretation.
- [ ] **12 - FastAPI service**: Expose analytics and predictions through REST API endpoints.
- [ ] **13 - Unit & integration tests**: Cover core data and analytics pipelines with pytest.
- [ ] **14 - Dockerization**: Containerize the application with Docker and Docker Compose.
- [ ] **15 - Documentation & CI/CD**: Finalize documentation and add GitHub Actions.

## Project Structure

```text
.
|-- data/
|   |-- raw/
|   `-- processed/
|-- src/
|   |-- __init__.py
|   |-- config.py
|   |-- data/
|   |-- analytics/
|   |-- ml/
|   `-- api/
|-- tests/
|-- .gitignore
|-- README.md
`-- requirements.txt
```

## Setup

```bash
git clone <url>
cd ecommerce-analytics
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```
