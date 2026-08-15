"""
Simple website scraper used by the Website Scraper Project.

Uses requests + BeautifulSoup to fetch a page and extract readable
text content, stripping out scripts, styles, images, and inputs.
"""

import requests
from bs4 import BeautifulSoup

# Standard browser-like headers so sites are less likely to block the request.
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
}

REQUEST_TIMEOUT = 10  # seconds
MAX_CONTENT_LENGTH = 2_000  # characters


def fetch_website_contents(url):
    """
    Return the title and text content of the website at the given URL,
    truncated to approximately 2,000 characters.
    """
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"

    if soup.body:
        # Remove elements that don't contribute readable text.
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""

    return (title + "\n\n" + text)[:MAX_CONTENT_LENGTH]


def fetch_website_links(url):
    """
    Return the list of link URLs (href values) found on the page at the given URL.

    Note: this parses the page separately from fetch_website_contents(),
    which is a bit inefficient, but kept simple for learning purposes.
    """
    response = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]