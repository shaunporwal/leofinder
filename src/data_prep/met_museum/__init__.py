"""
Metropolitan Museum of Art data preparation.

This package handles downloading and organizing
Met Museum Open Access dataset from Kaggle.
"""

from .download import download_met_dataset

__all__ = ['download_met_dataset']

