from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200, unique=True)
    type = models.CharField(max_length=50)
    author = models.CharField(max_length=150)
    release_date = models.DateField()
    publishing_company = models.CharField(max_length=11)
    synopsis = models.TextField()
    quantity = models.IntegerField()
    user = models.ManyToManyField(
        "users.User", through="Following", related_name="books"
    )


class Following(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="following"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="followers")


class Rating(models.Model):
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="book_ratings"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="ratings")
    rating = models.FloatField()
    description = models.TextField(null=True)
