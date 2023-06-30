from django.db import models


class Loan(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    devolution_date = models.DateTimeField()
    user = models.ForeignKey(
        "users.User", related_name="loans", on_delete=models.CASCADE
    )
    copy = models.ForeignKey(
        "copies.Copy", related_name="loans", on_delete=models.CASCADE
    )
