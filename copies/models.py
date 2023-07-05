from django.db import models
from rest_framework.validators import UniqueValidator
from books.models import Book


class Copy(models.Model):
    availability = models.BooleanField(default=True)
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="copies"
    )
