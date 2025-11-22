"""
Download the Metropolitan Museum of Art Open Access dataset from Kaggle.

This script downloads the Met Museum dataset, converts to parquet, and organizes it in the data directory.
"""

import kagglehub
import pandas as pd
import shutil
from pathlib import Path


def download_met_dataset():
    """
    Download the Met Museum dataset from Kaggle and move it to the data directory.
    
    Returns:
        Path: Path to the downloaded dataset
    """
    print("=" * 60)
    print("Downloading Met Museum Open Access Dataset from Kaggle...")
    print("=" * 60)
    
    # Download latest version from Kaggle
    kaggle_path = kagglehub.dataset_download("metmuseum/the-metropolitan-museum-of-art-open-access")
    
    print(f"\n✓ Downloaded to Kaggle cache: {kaggle_path}")
    
    # Get repo root (parent of src/)
    # __file__ is in src/data_prep/met_museum/, so go up 4 levels to reach repo root
    repo_root = Path(__file__).parent.parent.parent.parent
    target_dir = repo_root / "data" / "met-museum"
    
    # Create target directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy and convert files from Kaggle cache to our data directory
    kaggle_path_obj = Path(kaggle_path)
    
    print(f"\nProcessing files to: {target_dir}")
    print("=" * 60)
    
    files_processed = 0
    for file in kaggle_path_obj.iterdir():
        if file.is_file():
            if file.suffix == '.csv':
                # Convert CSV to Parquet
                print(f"Converting {file.name} to parquet...")
                # Read CSV with low_memory=False to handle mixed types
                df = pd.read_csv(file, low_memory=False)
                
                # Convert all columns to string to avoid type issues, then back to appropriate types
                # This handles mixed types gracefully
                for col in df.columns:
                    if df[col].dtype == 'object':
                        # Keep as string (will be stored efficiently in parquet)
                        df[col] = df[col].astype(str).replace('nan', None)
                
                parquet_file = target_dir / f"{file.stem}.parquet"
                df.to_parquet(parquet_file, index=False, engine='pyarrow')
                print(f"✓ Converted: {file.name} -> {parquet_file.name}")
                print(f"  Rows: {len(df):,}, Columns: {len(df.columns)}")
                files_processed += 1
            else:
                # Copy non-CSV files as-is
                target_file = target_dir / file.name
                shutil.copy2(file, target_file)
                print(f"Copied: {file.name}")
                files_processed += 1
    
    print("=" * 60)
    print(f"✓ Successfully processed {files_processed} files to {target_dir}")
    print(f"  Format: Parquet")
    
    return target_dir


if __name__ == "__main__":
    dataset_path = download_met_dataset()
    print(f"\n✓ Met Museum dataset is ready at: {dataset_path}")

