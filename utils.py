import requests
from requests.exceptions import RequestException

def fetch_html(url, retries=3):
    """
    Fetches the HTML content of a given URL.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.text
        except RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == retries - 1:
                print(f"Failed to fetch {url} after {retries} attempts.")
                return None

def clean_text(text):
    """
    Cleans extracted text by stripping whitespace.
    """
    if text:
        return text.strip()
    return ""
