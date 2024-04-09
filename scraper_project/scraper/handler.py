import csv
from .constants import BASE_URL


class ScraperHandler:
    def get_book_title(soup):
        h3_s = soup.find_all(
            "h3", attrs={"itemprop": "name", "class": "booktitle"})
        book_titles = []
        book_urls = []
        for h3 in h3_s:
            link = h3.find("a", attrs={"itemprop": "url", "class": "results"})
            book_title = link.get_text()
            book_titles.append(book_title)
            book_url = BASE_URL + link.get("href")
            book_urls.append(book_url)
        return book_titles, book_urls

    def get_book_author(soup):
        spans = soup.find_all(
            "span", attrs={"itemprop": "author", "class": "bookauthor"})
        authors_names = []
        authors_urls = []
        for span in spans:
            links = span.find_all("a", attrs={"class": "results"})
            authors_name = []
            authors_url = []
            for link in links:
                authors_name.append(link.get_text())
                authors_url.append(BASE_URL + link.get("href"))
            authors_names.append(authors_name)
            authors_urls.append(authors_url)
        return authors_names, authors_urls

    def get_book_cover(soup):
        spans = soup.find_all("span", attrs={"class": "bookcover"})
        book_covers = []
        for span in spans:
            a_tag = span.find("a")
            book_cover = a_tag.find("img", attrs={"itemprop": "image"})["src"]
            if book_cover[:7] == "/images":
                book_cover = BASE_URL + book_cover
            else:
                book_cover = "https:" + book_cover
            book_covers.append(book_cover)
        return book_covers

