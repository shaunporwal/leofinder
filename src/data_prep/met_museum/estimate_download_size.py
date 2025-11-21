"""
Estimate the total download size for Met Museum public domain images.
"""

import csv
import requests
from pathlib import Path
import random


def get_met_object_details(object_id):
    """Fetch object details from the Met Museum API."""
    api_url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    return response.json()


def estimate_download_size(sample_size=50):
    """
    Estimate total download size by sampling public domain objects.
    
    Args:
        sample_size: Number of objects to sample for size estimation
    """
    # Get repo root
    repo_root = Path(__file__).parent.parent.parent.parent
    csv_path = repo_root / "data" / "met-museum" / "MetObjects.csv"
    
    print("=" * 60)
    print("Estimating Met Museum Download Size")
    print("=" * 60)
    
    # Read all public domain object IDs
    public_domain_ids = []
    total_objects = 0
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_objects += 1
            if row['Is Public Domain'] == 'True':
                public_domain_ids.append(row['Object ID'])
    
    print(f"\nTotal objects in CSV: {total_objects:,}")
    print(f"Public domain objects: {len(public_domain_ids):,}")
    print(f"Percentage: {len(public_domain_ids)/total_objects*100:.1f}%")
    
    # Sample random objects
    sample_ids = random.sample(public_domain_ids, min(sample_size, len(public_domain_ids)))
    
    print(f"\nSampling {len(sample_ids)} random public domain objects...")
    print("=" * 60)
    
    total_size = 0
    objects_with_images = 0
    image_sizes = []
    
    for i, object_id in enumerate(sample_ids, 1):
        try:
            # Fetch details
            details = get_met_object_details(object_id)
            
            if details.get('primaryImage'):
                image_url = details['primaryImage']
                
                # Get image size without downloading full file (HEAD request)
                response = requests.head(image_url, timeout=10, allow_redirects=True)
                
                if response.status_code == 200 and 'content-length' in response.headers:
                    size = int(response.headers['content-length'])
                    total_size += size
                    image_sizes.append(size)
                    objects_with_images += 1
                    
                    print(f"[{i}/{len(sample_ids)}] Object {object_id}: {size/1024/1024:.2f} MB - {details.get('title', 'Untitled')[:50]}")
            else:
                print(f"[{i}/{len(sample_ids)}] Object {object_id}: No image")
                
        except Exception as e:
            print(f"[{i}/{len(sample_ids)}] Object {object_id}: Error - {e}")
            continue
    
    print("\n" + "=" * 60)
    print("ESTIMATION SUMMARY")
    print("=" * 60)
    
    if objects_with_images > 0:
        avg_size = total_size / objects_with_images
        availability_rate = objects_with_images / len(sample_ids)
        
        print(f"\nSample Statistics:")
        print(f"  Objects sampled: {len(sample_ids)}")
        print(f"  Objects with images: {objects_with_images}")
        print(f"  Image availability rate: {availability_rate*100:.1f}%")
        print(f"  Average image size: {avg_size/1024/1024:.2f} MB")
        print(f"  Median image size: {sorted(image_sizes)[len(image_sizes)//2]/1024/1024:.2f} MB")
        print(f"  Min image size: {min(image_sizes)/1024/1024:.2f} MB")
        print(f"  Max image size: {max(image_sizes)/1024/1024:.2f} MB")
        
        # Estimate total
        estimated_images = len(public_domain_ids) * availability_rate
        estimated_total_size = len(public_domain_ids) * availability_rate * avg_size
        
        print(f"\nEstimated Total Download:")
        print(f"  Estimated images available: {estimated_images:,.0f}")
        print(f"  Estimated total size: {estimated_total_size/1024/1024/1024:.1f} GB")
        print(f"  Estimated total size: {estimated_total_size/1024/1024/1024/1024:.2f} TB")
        
        # Time estimates
        print(f"\nEstimated Download Time:")
        # Assuming 10 MB/s average download speed
        download_speed_mbps = 10
        seconds = estimated_total_size / (download_speed_mbps * 1024 * 1024)
        hours = seconds / 3600
        days = hours / 24
        print(f"  At 10 MB/s: {hours:.1f} hours ({days:.1f} days)")
        
        # Assuming 50 MB/s fast connection
        download_speed_mbps = 50
        seconds = estimated_total_size / (download_speed_mbps * 1024 * 1024)
        hours = seconds / 3600
        print(f"  At 50 MB/s: {hours:.1f} hours ({hours/24:.1f} days)")
        
    else:
        print("\nNo images found in sample!")
    
    return {
        'total_public_domain': len(public_domain_ids),
        'objects_with_images': objects_with_images,
        'availability_rate': availability_rate if objects_with_images > 0 else 0,
        'avg_size_mb': avg_size/1024/1024 if objects_with_images > 0 else 0,
        'estimated_total_gb': estimated_total_size/1024/1024/1024 if objects_with_images > 0 else 0
    }


if __name__ == "__main__":
    estimate_download_size(sample_size=50)

