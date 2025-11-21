"""
Data preparation modules for artwork datasets.

This package contains:
- da_vinci: Leonardo da Vinci artwork from leonardoda-vinci.org
- met_museum: Metropolitan Museum of Art Open Access dataset
"""

# Re-export for backward compatibility and convenience
from .da_vinci import extract_image_data, download_images, save_manifest, sanitize_filename
from .met_museum import download_met_dataset

__all__ = [
    'extract_image_data',
    'download_images', 
    'save_manifest',
    'sanitize_filename',
    'download_met_dataset'
]

