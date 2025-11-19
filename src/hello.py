import requests
from bs4 import BeautifulSoup as bs

def main():
    url = "https://leonardoda-vinci.org/the-complete-works.html?ps=96"
    html = requests.get(url).text
    soup = bs(html, "html.parser")

    with open("/Users/shaunporwal/Desktop/leo-webpage.txt", "w", encoding="utf-8") as f:
        f.write(soup.prettify())

if __name__ == "__main__":
    main()
