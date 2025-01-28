# import asyncio
# import aiohttp
# from bs4 import BeautifulSoup
# import sqlite3
# from urllib.parse import urlparse, urljoin, urldefrag
# from tqdm import tqdm
# import logging

# # Logging configuration
# logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# logger = logging.getLogger(__name__)

# # Constants
# MAX_HEIGHT = 3
# CONCURRENT_REQUESTS = 10
# SEED_URLS = ["https://www.geeksforgeeks.org/dsa-tutorial-learn-data-structures-and-algorithms/"]

# # Semaphore to limit concurrent requests
# semaphore = asyncio.Semaphore(CONCURRENT_REQUESTS)


# def normalize_url(url):
#     """Normalize and clean URLs by removing fragments and trailing slashes."""
#     url = urldefrag(url)[0]  # Remove fragments
#     return url.rstrip("/")


# async def fetch(session, url):
#     """Fetch the content of a URL."""
#     try:
#         async with semaphore, session.get(url, ssl=False) as response:
#             response.raise_for_status()
#             content = await response.text()
#             return content
#     except Exception as e:
#         logger.error(f"Error fetching URL {url}: {e}")
#         return None


# async def extract_domain(url):
#     """Extract the domain of a given URL."""
#     try:
#         return "https://" + urlparse(url).netloc
#     except Exception as e:
#         logger.error(f"Error parsing URL: {e}")
#         return None


# async def extract_urls_from_page(session, url):
#     """Extract all valid URLs from a given page."""
#     try:
#         content = await fetch(session, url)
#         if not content:
#             return set()

#         soup = BeautifulSoup(content, "html.parser")
#         extracted_urls = set()

#         for link in soup.find_all("a"):
#             href = link.get("href")
#             if href:
#                 if href.startswith("#"):  # Skip fragments
#                     continue
#                 if href.startswith("/"):  # Handle relative URLs
#                     domain = await extract_domain(url)
#                     href = domain + href
#                 href = normalize_url(urljoin(url, href))  # Normalize URL
#                 extracted_urls.add(href)

#         return extracted_urls
#     except Exception as e:
#         logger.error(f"Error extracting URLs from {url}: {e}")
#         return set()


# async def extract_content(session, url):
#     """Extract clean text content from a URL."""
#     try:
#         content = await fetch(session, url)
#         if not content:
#             return ""

#         soup = BeautifulSoup(content, "html.parser")
#         for script in soup(["script", "style"]):
#             script.extract()  # Remove unnecessary tags

#         text = soup.get_text()
#         lines = (line.strip() for line in text.splitlines())
#         chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
#         cleaned_text = " ".join(chunk for chunk in chunks if chunk)
        
#         # Limit content size to avoid bloating
#         if len(cleaned_text) > 50000:
#             return cleaned_text[:50000] + " [Content Truncated]"
#         return cleaned_text
#     except Exception as e:
#         logger.error(f"Error extracting content from {url}: {e}")
#         return ""


# async def get_page_title(session, url):
#     """Extract the title of a webpage."""
#     try:
#         content = await fetch(session, url)
#         if not content:
#             return "Title Not Found"

#         soup = BeautifulSoup(content, "html.parser")
#         return soup.title.string if soup.title else "Title Not Found"
#     except Exception as e:
#         logger.error(f"Error extracting title from {url}: {e}")
#         return "Title Not Found"


# async def crawl_task(session, url, visited_urls, c):
#     """Crawl a single URL, extract its content, and store it in the database."""
#     visited_urls.add(url)
#     content = await extract_content(session, url)
#     title = await get_page_title(session, url)

#     try:
#         c.execute(
#             "INSERT OR IGNORE INTO url_data (url, content, title) VALUES (?, ?, ?)",
#             (url, content, title),
#         )
#     except sqlite3.Error as e:
#         logger.error(f"Database error for URL {url}: {e}")

#     new_urls = await extract_urls_from_page(session, url)
#     return new_urls


# async def crawl_urls(seed_urls):
#     """Crawl URLs starting from the seed URLs."""
#     conn = sqlite3.connect("crawled_urls.db")
#     c = conn.cursor()
#     c.execute(
#         """CREATE TABLE IF NOT EXISTS url_data (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            url TEXT UNIQUE,
#            content TEXT,
#            title TEXT
#        )"""
#     )

#     visited_urls = set()
#     urls = list(seed_urls)
#     height = 1

#     async with aiohttp.ClientSession() as session:
#         while urls:
#             total_urls = len(urls)
#             logger.info(f"Total URLs at height {height}: {total_urls}")

#             tasks = []
#             for _ in range(total_urls):
#                 current_url = urls.pop(0)
#                 if current_url not in visited_urls:
#                     tasks.append(asyncio.create_task(
#                         crawl_task(session, current_url, visited_urls, c)
#                     ))

#             new_urls = await asyncio.gather(*tasks)
#             urls.extend([url for sublist in new_urls for url in sublist if url not in visited_urls])

#             height += 1
#             if height > MAX_HEIGHT:
#                 logger.info(f"Crawler stopped at height {height}")
#                 break

#     conn.commit()
#     conn.close()


# if __name__ == "__main__":
#     asyncio.run(crawl_urls(SEED_URLS))


import asyncio
import aiohttp
from bs4 import BeautifulSoup
import sqlite3
from urllib.parse import urlparse, urljoin
from tqdm import tqdm


async def fetch(session, url):
    try:
        async with session.get(url, ssl=False) as response:  
            response.raise_for_status()
            content = await response.text()
            return content
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None





async def extract_domain(url):
    try:
        parsed_url = 'https://' + urlparse(url).netloc
        return parsed_url
    except Exception as e:
        print(f"Error parsing URL: {e}")
        return None





async def extract_urls_from_page(session, url):
    try:
        content = await fetch(session, url)
        if not content:
            return set()

        soup = BeautifulSoup(content, 'html.parser')
        extracted_urls = set()
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                if href[0] == "#":
                    continue
                if href[0] == "/":
                    domain = await extract_domain(url)
                    href = domain + href
                href = urljoin(href, urlparse(href).path)
                extracted_urls.add(href)
        return extracted_urls
    except Exception as e:
        print(f"Error extracting URLs from {url}: {e}")
        return set()

async def extract_content(session, url):
    try:
        content = await fetch(session, url)
        if not content:
            return ''

        soup = BeautifulSoup(content, "html.parser")
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split(" "))
        cleaned_text = " ".join(chunk for chunk in chunks if chunk)
        return cleaned_text
    except Exception as e:
        print(f"Error extracting content from {url}: {e}")
        return ''


async def get_page_title(session, url):
    try:
        content = await fetch(session, url)
        if not content:
            return "Title Not Found"

        soup = BeautifulSoup(content, 'html.parser')
        title = soup.title.string
        return title
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return "Title Not Found"

async def crawl_task(session, url, visited_urls, c):
    visited_urls.add(url)
    content = await extract_content(session, url)
    title = await get_page_title(session, url)
    c.execute(
        "INSERT OR IGNORE INTO url_data (url, content, title) VALUES (?, ?, ?)",
          (url, content, title))
    new_urls = await extract_urls_from_page(session, url)
    return new_urls

async def crawl_urls(urls):
    conn = sqlite3.connect('crawled_urls.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS url_data 
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              url TEXT UNIQUE, content TEXT, title TEXT)''')

    visited_urls = set()
    height = 1
    async with aiohttp.ClientSession() as session:
        while urls:
            total_urls = len(urls)
            tasks = []
            for _ in range(total_urls):
                current_url = urls.pop(0)
                if current_url not in visited_urls:
                    tasks.append(asyncio.ensure_future(
                        crawl_task(session, current_url, visited_urls, c)))
            new_urls = await asyncio.gather(*tasks)
            urls.extend([url for sublist in new_urls for url in sublist]) 
            height += 1
            print(f"Total urls at height {height} : {total_urls} ")
            if height == max_height:
                print(f"Crawler Stopped At Height {height}")
                break

    conn.commit()
    conn.close()

if __name__ == "__main__":
    max_height = 3
    seed_urls = ["https://www.geeksforgeeks.org/dsa-tutorial-learn-data-structures-and-algorithms/"]
    asyncio.run(crawl_urls(seed_urls))