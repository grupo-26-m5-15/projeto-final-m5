from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=100, null=False)
    cnpj = models.CharField(max_length=14, null=False, unique=True)
    email = models.CharField(max_length=150, null=False, unique=True)
    address = models.CharField(max_length=200)

    employees = models.ManyToManyField(
        "users.User", through="LibraryEmployee", related_name="my_library"
    )


class LibraryEmployee(models.Model):
    library = models.ForeignKey(
        Library, on_delete=models.CASCADE
    )
    employee = models.ForeignKey(
        "users.User", on_delete=models.CASCADE
    )
    is_employee = models.BooleanField(default=True, null=False)


class LibraryBooks(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="books")
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="libraries"
    )


class UserLibraryBlock(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name="users")
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="libraries_blocked"
    )
    is_blocked = models.BooleanField(default=False)
