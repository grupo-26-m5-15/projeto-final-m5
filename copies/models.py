from django.db import models


class Copy(models.Model):
    quantity = models.IntegerField()
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="copies"
    )
