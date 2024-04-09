from django.urls import path
from .views import BooksView, ScraperView

urlpatterns = [
    path('scraper/', ScraperView.as_view(), name='scraper'),
    path('scraper/books/', BooksView.as_view(), name='books'),
]
