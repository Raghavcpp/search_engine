import requests
from bs4 import BeautifulSoup

def extract_urls_from_page(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        
        # Parse the response content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        extracted_urls = set()  # Use a set to avoid duplicate URLs
        for link in soup.find_all('a'):  # Find all <a> tags
            href = link.get('href')  # Extract the href attribute
            if href and href.startswith("http"):  # Filter for absolute URLs
                extracted_urls.add(href)
        
        return extracted_urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return set()

# Define the seed URL
seed_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"

# Call the function to extract URLs
urls = extract_urls_from_page(seed_url)

# Write the extracted URLs to a file
with open("urls.txt", "w") as file:
    for item in urls:
        file.write(f"{item}\n")
