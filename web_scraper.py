import csv
import requests
from bs4 import BeautifulSoup


def scrape_quotes():
  # Target URL (A live legal practice site for scraping)
  url = "http://quotes.toscrape.com/"

  # Professional headers taake server ko lage ke request browser se aa rahi hai
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  print("[*] Connecting to the website...")
  try:
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code != 200:
      print(f"[!] Failed to retrieve data. Status code: {response.status_code}")
      return

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")
    quotes_data = []

    # Find all quote containers on the page
    quote_boxes = soup.find_all("div", class_="quote")
    print(f"[+] Found {len(quote_boxes)} quotes. Extracting data...")

    for box in quote_boxes:
      # Extracting text and author
      quote = box.find("span", class_="text").get_text(strip=True)
      author = box.find("small", class_="author").get_text(strip=True)

      # Extracting associated tags
      tags = [
          tag.get_text(strip=True) for tag in box.find_all("a", class_="tag")
      ]

      # Storing structured dictionary
      quotes_data.append(
          {"Quote": quote, "Author": author, "Tags": ", ".join(tags)}
      )

    # Data Processing & Saving to CSV
    filename = "scraped_quotes.csv"
    print(f"[*] Processing and saving data to {filename}...")

    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
      fieldnames = ["Quote", "Author", "Tags"]
      writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

      writer.writeheader()
      for item in quotes_data:
        writer.writerow(item)

    print(f"[✔] Success! Data saved as {filename}.")

  except requests.exceptions.RequestException as e:
    print(f"[!] Network or connection error occurred: {e}")


if __name__ == "__main__":
  scrape_quotes()