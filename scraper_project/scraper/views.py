import asyncio
import aiohttp
from bs4 import BeautifulSoup
from django.views.generic import FormView, TemplateView
from asgiref.sync import sync_to_async

from .handler import ScraperHandler
from .forms import SearchForm
from .models import Book, Author
from django.core.paginator import Paginator


class ScraperView(FormView):
    template_name = 'scraper.html'
    form_class = SearchForm
    success_url = 'books/'

    async def fetch_page(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    async def scrape_page(self, search_subject, page_number):
        url = f"https://openlibrary.org/search?q={search_subject}&page={page_number}"
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_page(session, url)
            soup = BeautifulSoup(html, "html.parser")
            book_titles, book_urls = ScraperHandler.get_book_title(soup)
            authors_names, authors_urls = ScraperHandler.get_book_author(soup)
            book_covers = ScraperHandler.get_book_cover(soup)

            for title, url, cover in zip(book_titles, book_urls, book_covers):
                book = await sync_to_async(Book.objects.create)(title=title, url=url, cover=cover)
                for author_name, author_url in zip(authors_names, authors_urls):
                    author, _ = await sync_to_async(Author.objects.get_or_create)(name=author_name, url=author_url)
                    await sync_to_async(author.books.add)(book)

    async def scrape_pages(self, search_subject, search_page_count):
        tasks = []
        print("Scraping... Please wait...")
        for page_number in range(1, search_page_count + 1):
            task = asyncio.create_task(
                self.scrape_page(search_subject, page_number))
            tasks.append(task)
        await asyncio.gather(*tasks)
        print("Done!")

    def form_valid(self, form):
        search_subject = form.cleaned_data['search_subject'] or 'music'
        search_page_count = form.cleaned_data['search_page_count'] or 1
        asyncio.run(self.scrape_pages(search_subject, search_page_count))
        return super().form_valid(form)


class BooksView(TemplateView):
    # template_name = 'books.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['books'] = Book.objects.all()
    #     return context

    template_name = 'books.html'
    paginate_by = 5  # Number of books to display per page

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_books = Book.objects.all()
        paginator = Paginator(all_books, self.paginate_by)
        page_number = self.request.GET.get('page')
        books = paginator.get_page(page_number)
        context['books'] = books
        return context
