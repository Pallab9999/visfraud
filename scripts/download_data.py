from pathlib import Path
import sys

try:
    from kaggle import KaggleApi
except ImportError:
    raise SystemExit(
        "Missing dependency: install the Kaggle API client with `pip install kaggle` before running this script."
    )


def download_creditcard_csv(data_dir: Path, force: bool = False) -> Path:
    data_dir.mkdir(parents=True, exist_ok=True)
    target_file = data_dir / "creditcard.csv"
    if target_file.exists() and not force:
        print(f"Dataset already exists at {target_file}")
        return target_file

    api = KaggleApi()
    api.authenticate()
    dataset_ref = "mlg-ulb/creditcardfraud"
    print(f"Downloading creditcard.csv from Kaggle dataset '{dataset_ref}'...")
    api.dataset_download_file(dataset_ref, file_name="creditcard.csv", path=str(data_dir), force=force)

    possible_zip = data_dir / "creditcard.csv.zip"
    if possible_zip.exists():
        import zipfile

        print(f"Extracting archive {possible_zip}...")
        with zipfile.ZipFile(possible_zip, "r") as zip_ref:
            zip_ref.extractall(path=str(data_dir))
        possible_zip.unlink()

    if not target_file.exists():
        raise SystemExit(
            "Download completed but creditcard.csv was not found in the data directory."
        )

    print(f"Downloaded dataset to {target_file}")
    return target_file


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Download the Kaggle Credit Card Fraud dataset to the local data/ directory."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Redownload the dataset even if creditcard.csv already exists.",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data"
    download_creditcard_csv(data_path, force=args.force)
