# This script collects links to audiobooks on everend.com. These audiobooks can be then scraped by using audiobook-dl (https://github.com/jo1gi/audiobook-dl).
# Example command:
# audiobook-dl -c everand_cookies.txt --username YOURUSERNAME --password YOURPASSWORD --input-file audiobook_links.txt

import asyncio
from playwright.async_api import async_playwright

async def extract_book_links(page_num):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Here is the url of your search page on Everend. Insert your url. 
        # I was searching for Hungarian audiobooks.
        url = f'https://www.everand.com/search?query=a&content_type=audiobooks&filters=%7B%22language%22%3A%5B%2219%22%5D%7D&page={page_num}'
        await page.goto(url)

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

async def main():
    all_links = []
    for page_num in range(1, 10):  # for English 238. Adjust range as needed for the number of pages. Seems like Everend has a limit of pages you can view even if more pages with books are available.
        page_links = await extract_book_links(page_num)
        all_links.extend(page_links)

    # Write collected links to a .txt file
    with open('audiobook_links.txt', 'w') as file:
        for link in all_links:
            if link.startswith('https://www.everand.com/audiobook/'): # Discarding book series
                # file.write(link + '\n') # Outputs a list of Audiobook pages
                # file.write(link[34:43] + ' - ' + link[44:] + '\n') # Outputs a list of book IDs and titles for your reference
                file.write('https://www.everand.com/listen/' + link[34:43] + '\n') # Outputs a list of Audiobook listening pages for audiobook-dl

asyncio.run(main())
