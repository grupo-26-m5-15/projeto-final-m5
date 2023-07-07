from django.db import models


class Loan(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    devolution_date = models.DateTimeField()
    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="loans"
    )
    copy = models.ForeignKey(
        "copies.Copy", on_delete=models.CASCADE, related_name="loans"
    )