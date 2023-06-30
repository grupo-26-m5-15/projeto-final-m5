from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=100, null=False)
    cnpj = models.CharField(max_length=11, null=False, unique=True)
    email = models.CharField(max_length=150, null=False, unique=True)
    address = models.CharField(max_length=200)


class LibraryEmployee(models.Model):
    library = models.ForeignKey(Library, related_name="libraries")
    employee = models.ForeignKey("users.User", related_name="libraries")
    is_employee = models.BooleanField(default=True, null=False)


class LibraryBooks(models.Model):
    library = models.ForeignKey(Library, related_name="books")
    book = models.ForeignKey("books.Book", related_name="libraries")


class UserLibraryBlock(models.Model):
    library = models.ForeignKey(Library, related_name="users")
    user = models.ForeignKey("users.User", related_name="libraries")
    is_blocked = models.BooleanField(default=False)
