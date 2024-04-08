from django.db import models


class MyBaseModel(models.Model):
    is_active = models.BooleanField(
        default=False,
        verbose_name="Is Active",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Updated At",
    )

    class Meta:
        abstract = True
        ordering = ("pk",)

    def __str__(self):
        raise NotImplementedError("Implement __str__ method")


class Author(MyBaseModel):
    name = models.CharField(max_length=1000, null=True,
                            blank=True, verbose_name="Name")
    url = models.URLField(null=True, blank=True, verbose_name="URL")

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"
        ordering = ("id",)

    def __str__(self) -> str:
        return self.name


class Book(MyBaseModel):
    title = models.CharField(max_length=1000, null=True,
                             blank=True, verbose_name="Title")
    url = models.URLField(null=True, blank=True, verbose_name="URL")
    cover = models.URLField(null=True, blank=True, verbose_name="Cover")
    author = models.ForeignKey(Author, null=True, blank=True,
                               on_delete=models.PROTECT, related_name="books", verbose_name="Author")

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ("id",)

    def __str__(self) -> str:
        return self.title
