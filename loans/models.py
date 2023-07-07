from django.db import models
from dateutil.relativedelta import relativedelta


class Loan(models.Model):
    start_date = models.DateTimeField(auto_now_add=True)

    end_date = models.DateTimeField(null=True)
    devolution_date = models.DateTimeField(null=True)

    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="loan"
    )

    copy = models.ForeignKey(
        "copies.Copy", on_delete=models.PROTECT, related_name="loan"
    )

    library = models.ForeignKey(
        "libraries.Library", on_delete=models.CASCADE, related_name="loan"
    )
