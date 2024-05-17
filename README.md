# Everend audiobooks scraper

A tool for scraping audiobook links from **[Everend](https://www.everand.com/home)** for downloading them with **[audiobook-dl](https://github.com/jo1gi/audiobook-dl)**.

## Usage: 
```
python get_audiobook_links.py <url> <output_file> [num_pages]
```

## Output:
A .txt file with links to audiobook listen pages, each link in a separate raw.
```
https://www.everand.com/listen/BOOK_ID_01
https://www.everand.com/listen/BOOK_ID_02
...
```

## Example of downloading:
```
audiobook-dl -c everand_cookies.txt --username YOURUSERNAME --password YOURPASSWORD --input-file audiobook_links.txt
```

