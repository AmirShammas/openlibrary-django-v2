from django.contrib import admin
from django.contrib.admin import register
from .models import Author, Book


@register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url", "is_active",
                    "created_at", "updated_at")
    list_display_links = ("id", "name")
    list_filter = ("is_active", "created_at", "updated_at")
    list_editable = ("is_active",)
    search_fields = ("name",)


@register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "url", "cover", "author",
                    "is_active", "created_at", "updated_at")
    list_display_links = ("id", "title")
    list_filter = ("is_active", "created_at", "updated_at", "author",)
    list_editable = ("is_active",)
    search_fields = ("title", "is_active", "author__name",)
