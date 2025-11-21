"""
Test script to check if we can download images from the Met Museum API.

The Met Museum provides an API that gives access to high-resolution images
for objects in their open access collection.
"""

import csv
import requests
from pathlib import Path


def get_met_object_details(object_id):
    """
    Fetch object details from the Met Museum API.
    
    Args:
        object_id: The Object ID from the CSV
    
    Returns:
        dict: Object details including image URL
    """
    api_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()


def test_download_one_image():
    """
    Test downloading one image from the Met Museum collection.
    """
    # Get repo root
    repo_root = Path(__file__).parent.parent.parent.parent
    csv_path = repo_root / "data" / "met-museum" / "MetObjects.csv"
    
    print("=" * 60)
    print("Testing Met Museum Image Download")
    print("=" * 60)
    
    # Read the CSV and find a public domain object with a highlight
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            # Look for a highlighted public domain object
            if row['Is Highlight'] == 'True' and row['Is Public Domain'] == 'True':
                object_id = row['Object ID']
                title = row['Title']
                
                print(f"\nFound object:")
                print(f"  Object ID: {object_id}")
                print(f"  Title: {title}")
                print(f"  Artist: {row['Artist Display Name']}")
                
                # Fetch object details from API
                print(f"\nFetching details from Met API...")
                try:
                    details = get_met_object_details(object_id)
                    
                    # Check if there's a primary image
                    if details.get('primaryImage'):
                        image_url = details['primaryImage']
                        print(f"  Primary Image URL: {image_url}")
                        
                        # Try to download the image
                        print(f"\nDownloading image...")
                        response = requests.get(image_url, timeout=30)
                        response.raise_for_status()
                        
                        # Save to test location
                        test_dir = repo_root / "data" / "met-museum" / "test"
                        test_dir.mkdir(exist_ok=True)
                        
                        image_path = test_dir / f"test_object_{object_id}.jpg"
                        with open(image_path, 'wb') as img_file:
                            img_file.write(response.content)
                        
                        print(f"✓ Successfully downloaded image to: {image_path}")
                        print(f"  File size: {len(response.content) / 1024:.1f} KB")
                        
                        # Show what metadata is available
                        print(f"\nAvailable metadata from API:")
                        print(f"  Object Date: {details.get('objectDate')}")
                        print(f"  Medium: {details.get('medium')}")
                        print(f"  Dimensions: {details.get('dimensions')}")
                        print(f"  Department: {details.get('department')}")
                        print(f"  Is Public Domain: {details.get('isPublicDomain')}")
                        
                        return True
                    else:
                        print(f"  No primary image available for this object")
                        continue
                        
                except Exception as e:
                    print(f"  Error: {e}")
                    continue
                
        print("\nNo suitable objects found")
        return False


if __name__ == "__main__":
    test_download_one_image()

