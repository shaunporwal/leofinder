import requests
from bs4 import BeautifulSoup as bs


def extract_image_data():
    """
    Scrapes all Leonardo da Vinci artwork images from leonardoda-vinci.org.
    
    Returns:
        dict: Dictionary with artwork titles as keys and image URLs as values.
    """
    # 1. Define the Base URL for constructing absolute links
    BASE_URL = "https://leonardoda-vinci.org"
    
    # 2. Define all page URLs
    page_urls = [
        "https://leonardoda-vinci.org/the-complete-works.html?ps=96",
        "https://leonardoda-vinci.org/the-complete-works_pageno-2.html?ps=96",
        "https://leonardoda-vinci.org/the-complete-works_pageno-3.html?ps=96",
        "https://leonardoda-vinci.org/the-complete-works_pageno-4.html?ps=96"
    ]
    
    extracted_data = {}
    
    # 3. Loop through all pages
    for page_num, url in enumerate(page_urls, 1):
        print(f"\nFetching page {page_num}...")
        
        # Fetch HTML and create the soup object
        try:
            html = requests.get(url).text
            soup = bs(html, "html.parser")
        except requests.RequestException as e:
            print(f"Error fetching page {page_num} ({url}): {e}")
            continue  # Skip to next page if this one fails

        # Find the main container holding all the artwork listings
        items_container = soup.find('div', class_='row items-list-wrapper')

        if not items_container:
            print(f"Warning: Could not find artwork container on page {page_num}")
            continue

        # Find all <img> tags within the container
        image_tags = items_container.find_all('img')
        
        print(f"Found {len(image_tags)} images on page {page_num}")
        
        # Iterate and extract the required attributes
        for img_tag in image_tags:
            # Get the relative URL from the 'src' attribute
            relative_path = img_tag.get('src')
            
            # Get the title from the 'alt' attribute
            title = img_tag.get('alt', '').strip()
            
            if relative_path and title:  # Only add if both title and path exist
                # Construct the absolute URL
                absolute_url = BASE_URL + relative_path
                
                # Add to dictionary: key = title, value = absolute URL
                extracted_data[title] = absolute_url

    return extracted_data

