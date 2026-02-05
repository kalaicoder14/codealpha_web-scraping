import csv
import os
from bs4 import BeautifulSoup
from utils import fetch_html, clean_text

class QuoteScraper:
    def __init__(self, base_url):
        self.base_url = base_url
        self.data = []

    def scrape_page(self, page_number=1):
        """
        Scrapes a single page of quotes.
        """
        url = f"{self.base_url}/page/{page_number}/"
        print(f"Scraping {url}...")
        
        html_content = fetch_html(url)
        if not html_content:
            return False

        # Use html.parser which is built-in
        soup = BeautifulSoup(html_content, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        if not quotes:
            print("No quotes found on this page.")
            return False

        for quote in quotes:
            text = clean_text(quote.find('span', class_='text').text)
            author = clean_text(quote.find('small', class_='author').text)
            # Safe handling if tags are missing or structure differs
            tags_container = quote.find('div', class_='tags')
            tags = [tag.text for tag in tags_container.find_all('a', class_='tag')] if tags_container else []
            
            self.data.append({
                'text': text,
                'author': author,
                'tags': ", ".join(tags)
            })
        
        return True

    def run(self, max_pages=5):
        """
        Runs the scraper for a limited number of pages.
        """
        for page in range(1, max_pages + 1):
            if not self.scrape_page(page):
                break
        
        self.save_data()

    def save_data(self):
        """
        Saves the collected data to a CSV file using the csv module.
        """
        if not self.data:
            print("No data collected to save.")
            return

        # Ensure output directory exists
        output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'processed')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'quotes.csv')
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                # Get headers from the first dictionary keys
                fieldnames = self.data[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(self.data)
                
            print(f"Data saved to {output_file}")
            print(f"Total quotes scraped: {len(self.data)}")
        except IOError as e:
            print(f"Error saving file: {e}")

if __name__ == "__main__":
    BASE_URL = "http://quotes.toscrape.com"
    scraper = QuoteScraper(BASE_URL)
    scraper.run(max_pages=3)
