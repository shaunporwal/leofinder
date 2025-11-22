import pandas as pd
import requests
from pathlib import Path


def sanitize_filename(filename):
    """
    Sanitize filename by replacing invalid characters and spaces with dashes.
    """
    # Replace invalid characters with underscores
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Replace spaces with dashes for cleaner filenames
    filename = filename.replace(' ', '-')
    
    # Replace multiple dashes with single dash
    while '--' in filename:
        filename = filename.replace('--', '-')
    
    return filename


def download_images(image_info, output_dir='data/da-vinci-works'):
    """
    Download all images from the image_info dictionary and create a manifest.
    
    Args:
        image_info: Dictionary with artwork titles as keys and URLs as values
        output_dir: Directory to save images (relative to repo root)
    
    Returns:
        list: Manifest data with metadata for each image
    """
    # Get repo root (parent of src/)
    # __file__ is in src/data_prep/da_vinci/, so go up 4 levels to reach repo root
    repo_root = Path(__file__).parent.parent.parent.parent
    data_dir = repo_root / output_dir
    
    # Create data directory if it doesn't exist
    data_dir.mkdir(exist_ok=True)
    print(f"Saving images to: {data_dir}")
    print("=" * 60)
    
    total_images = len(image_info)
    successful = 0
    failed = 0
    manifest = []
    
    for i, (title, url) in enumerate(image_info.items(), 1):
        # Sanitize the title to make it a valid filename
        safe_title = sanitize_filename(title)
        
        # Get file extension from URL (usually .jpg)
        file_ext = '.jpg'
        if '.' in url:
            file_ext = '.' + url.split('.')[-1].split('?')[0]  # Handle URL params
        
        # Create filename
        filename = f"{safe_title}{file_ext}"
        filepath = data_dir / filename
        
        # Create manifest entry
        manifest_entry = {
            "id": i,
            "filename": filename,
            "original_title": title,
            "url": url,
            "status": "unknown",
            # Placeholder fields for future metadata
            "year": None,
            "source": None,
            "medium": None,
            "dimensions": None,
            "location": None,
            "notes": None
        }
        
        # Check if file already exists
        if filepath.exists():
            print(f"[{i}/{total_images}] Skipping (already exists): {safe_title}")
            manifest_entry["status"] = "success"
            successful += 1
            manifest.append(manifest_entry)
            continue
        
        # Download the image
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            # Save the image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"[{i}/{total_images}] Downloaded: {safe_title}")
            manifest_entry["status"] = "success"
            successful += 1
            
        except Exception as e:
            print(f"[{i}/{total_images}] Failed to download {safe_title}: {e}")
            manifest_entry["status"] = "failed"
            manifest_entry["error"] = str(e)
            failed += 1
        
        manifest.append(manifest_entry)
    
    print("\n" + "=" * 60)
    print(f"✓ Download complete!")
    print(f"  Successful: {successful}/{total_images}")
    print(f"  Failed: {failed}/{total_images}")
    print(f"  Location: {data_dir}")
    
    return manifest


def save_manifest(manifest, output_dir='data/da-vinci-works', output_file='manifest.parquet'):
    """
    Save the manifest to a parquet file in the data directory.
    
    Args:
        manifest: List of manifest entries
        output_dir: Directory to save manifest (relative to repo root)
        output_file: Filename for the manifest
    """
    # Get repo root (parent of src/)
    # __file__ is in src/data_prep/da_vinci/, so go up 4 levels to reach repo root
    repo_root = Path(__file__).parent.parent.parent.parent
    data_dir = repo_root / output_dir
    manifest_path = data_dir / output_file
    
    # Convert manifest list to DataFrame and save as parquet
    df = pd.DataFrame(manifest)
    df.to_parquet(manifest_path, index=False, engine='pyarrow')
    
    print(f"\n✓ Manifest saved to: {manifest_path}")
    print(f"  Total entries: {len(manifest)}")
    print(f"  Format: Parquet")

