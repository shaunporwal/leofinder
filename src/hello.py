import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_soup(url):
    """Fetches a URL and returns a BeautifulSoup object."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.content, 'html.parser')
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def main():
    base_url = "https://leonardoda-vinci.org"
    gallery_url = f"{base_url}/the-complete-works.html?ps=96"
    
    print(f"Fetching gallery page: {gallery_url}")
    soup = get_soup(gallery_url)
    if not soup:
        return

    # Find all artwork links. 
    # Based on typical gallery structures, we look for links that might be artworks.
    # The user mentioned links like /The-Last-Supper-1498.html
    artwork_links = []
    
    # This selector might need adjustment based on the actual page structure.
    # Looking for 'a' tags where href ends in .html and doesn't look like a utility link.
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Filter out common non-artwork links if possible, or just try to visit them.
        # A simple heuristic: relative links ending in .html, not index.html, etc.
        if href.endswith('.html') and 'complete-works' not in href and 'index' not in href and 'biography' not in href:
             # Ensure it's a full URL
            full_url = urllib.parse.urljoin(base_url, href)
            if full_url not in artwork_links:
                artwork_links.append(full_url)

    print(f"Found {len(artwork_links)} potential artwork pages.")

    for i, link in enumerate(artwork_links):
        print(f"[{i+1}/{len(artwork_links)}] Processing {link}...")
        art_soup = get_soup(link)
        if not art_soup:
            continue
            
        # Find the high-res image.
        # User said: "Find the image tag (usually <img> or a <div> with a background image). The link in the src attribute"
        # We'll look for the main image. Often it's the largest image or inside a specific container.
        # Without the live page, we'll try a few common patterns.
        
        # Strategy 1: Look for an image with a src that looks like an upload/gallery image, not a layout asset.
        # Strategy 2: Look for the largest image?
        # Strategy 3: Look for 'img' tags inside a main content area.
        
        found_img = None
        images = art_soup.find_all('img', src=True)
        
        # Heuristic: filter out small icons, logos, etc. if possible. 
        # Or look for images that don't have 'thumb' in the name?
        # The user example was .../base_6796027.jpg?width=300 for thumb.
        # We want the one without width limit or the main one.
        
        for img in images:
            src = img['src']
            # Skip common layout images
            if 'logo' in src.lower() or 'icon' in src.lower() or 'spacer' in src.lower():
                continue
            
            # Construct full URL
            full_img_url = urllib.parse.urljoin(base_url, src)
            
            # If we find a likely candidate, print it.
            # For now, let's print the first likely candidate or all of them?
            # Better to be verbose than miss it.
            print(f"  Found image: {full_img_url}")
            # In a real scenario, we might want to download it or just list it.
            
            # If we assume there's one main image per page, we might stop after finding a "good" one.
            # But let's just list them for now as requested.

if __name__ == "__main__":
    main()
