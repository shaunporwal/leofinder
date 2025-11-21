"""
Download the Metropolitan Museum of Art Open Access dataset from Kaggle.

This script downloads the Met Museum dataset and organizes it in the data directory.
"""

import kagglehub
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
    
    # Copy files from Kaggle cache to our data directory
    kaggle_path_obj = Path(kaggle_path)
    
    print(f"\nCopying files to: {target_dir}")
    print("=" * 60)
    
    files_copied = 0
    for file in kaggle_path_obj.iterdir():
        if file.is_file():
            target_file = target_dir / file.name
            shutil.copy2(file, target_file)
            print(f"Copied: {file.name}")
            files_copied += 1
    
    print("=" * 60)
    print(f"✓ Successfully copied {files_copied} files to {target_dir}")
    
    return target_dir


if __name__ == "__main__":
    dataset_path = download_met_dataset()
    print(f"\n✓ Met Museum dataset is ready at: {dataset_path}")

