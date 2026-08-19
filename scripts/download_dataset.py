import shutil
import sys
import time
from http.client import IncompleteRead
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen
from zipfile import ZipFile

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

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
    retries = 3

    for attempt in range(1, retries + 1):
        try:
            with urlopen(DATASET_URL) as response, open(ARCHIVE_PATH, "wb") as archive_file:
                shutil.copyfileobj(response, archive_file)
            break
        except (IncompleteRead, HTTPError, URLError, TimeoutError, OSError) as exc:
            if attempt == retries:
                raise RuntimeError(f"Failed to download dataset after {retries} attempts") from exc
            print(f"Download attempt {attempt} failed: {exc}. Retrying...")
            time.sleep(2)

    with ZipFile(ARCHIVE_PATH) as archive:
        archive.extract(DATASET_FILENAME, RAW_DATA_DIR)

    print(f"Dataset saved to: {DATASET_PATH}")
    return DATASET_PATH


if __name__ == "__main__":
    download_dataset()
