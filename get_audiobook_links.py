# This script scrapes links to audiobooks on everend.com.
# These audiobooks can be downloaded using audiobook-dl (https://github.com/jo1gi/audiobook-dl). 
# Example command:
# audiobook-dl -c everand_cookies.txt --username YOURUSERNAME --password YOURPASSWORD --input-file audiobook_links.txt

import sys
import asyncio
from playwright.async_api import async_playwright

async def extract_book_links(page_num, url):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        url_with_page = f'{url}&page={page_num}'
        await page.goto(url_with_page)

        # Wait for book links to be loaded
        try:
            await page.wait_for_selector('[class^="FluidCell-module_linkOverlay__"]', timeout=30000)  # Increased timeout to 60 seconds
        except Exception as e:
            print(f"Timeout waiting for selector: {e}")

        # Extract book links
        book_links = await page.evaluate('''() => {
            const links = Array.from(document.querySelectorAll('[class^="FluidCell-module_linkOverlay__"]'));
            return links.map(link => link.href);
        }''')

        await browser.close()
        return book_links

async def main(url, output_file, num_pages):
    tasks = []
    for page_num in range(1, num_pages + 1):
        tasks.append(extract_book_links(page_num, url))

    all_links = await asyncio.gather(*tasks)

    # Flatten the list of lists
    all_links_flat = [link for sublist in all_links for link in sublist]

    # Write collected links to the specified .txt file
    with open(output_file, 'w') as file:
        for link in all_links_flat:
            if link.startswith('https://www.everand.com/audiobook/'):
                file.write('https://www.everand.com/listen/' + link[34:43] + '\n')
                #file.write(link + '\n') # If you want a list of book numeric IDs
                #file.write(link[34:43] + ' - ' + link[44:] + '\n') # If you want a list of numeric IDs and book titles

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: python script.py <url> <output_file> [num_pages]")
    else:
        url = sys.argv[1]
        output_file = sys.argv[2]
        num_pages = int(sys.argv[3]) if len(sys.argv) == 4 else float('inf')  # Default: scrape all available pages
        asyncio.run(main(url, output_file, num_pages))


