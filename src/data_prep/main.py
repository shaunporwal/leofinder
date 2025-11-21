"""
Main entry point for the Leonardo da Vinci artwork scraper and downloader.

This script orchestrates the complete workflow:
1. Scrapes artwork data from leonardoda-vinci.org
2. Downloads all images
3. Creates a manifest file with metadata
"""

from scraper import extract_image_data
from downloader import download_images, save_manifest


if __name__ == "__main__":
    print("Starting to extract images from all 4 pages...")
    print("=" * 60)
    
    image_info = extract_image_data()
    
    print("\n" + "=" * 60)
    print(f"Total artworks found: {len(image_info)}")
    print("=" * 60)
    
    # Download all images and get manifest data
    manifest = download_images(image_info)
    
    # Save manifest to JSON file
    save_manifest(manifest)
