from django.db import models


class Copy(models.Model):
    quantity = models.IntegerField()
    book = models.ForeignKey(
        "books.Book", related_name="copies", on_delete=models.CASCADE
    )
