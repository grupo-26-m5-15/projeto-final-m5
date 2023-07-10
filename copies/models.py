from django.db import models
from rest_framework.validators import UniqueValidator

from books.models import Book


class Copy(models.Model):
    is_available = models.BooleanField(default=True, null=True)

    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="copies"
    )
