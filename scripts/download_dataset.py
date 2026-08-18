from pathlib import Path
from urllib.request import urlretrieve
from zipfile import ZipFile

from src.config import RAW_DATA_DIR
from src.data.schema import DATASET_URL


ARCHIVE_PATH = RAW_DATA_DIR / "online_retail_ii.zip"
DATASET_FILENAME = "online_retail_II.xlsx"
DATASET_PATH = RAW_DATA_DIR / DATASET_FILENAME


def download_dataset() -> Path:
    """Download and extract the Online Retail II dataset from UCI."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    if DATASET_PATH.exists():
        print(f"Dataset already exists: {DATASET_PATH}")
        return DATASET_PATH

    print(f"Downloading dataset from {DATASET_URL}")
    urlretrieve(DATASET_URL, ARCHIVE_PATH)

    with ZipFile(ARCHIVE_PATH) as archive:
        archive.extract(DATASET_FILENAME, RAW_DATA_DIR)

    print(f"Dataset saved to: {DATASET_PATH}")
    return DATASET_PATH


if __name__ == "__main__":
    download_dataset()
