
from libraries.models import UserLibraryBlock

import calendar
from datetime import date, datetime as dt
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from books.models import Following
from django.core.mail import send_mail


class Dates():
    today = timezone.now()

    def devolution_date(self, day=15):
        end_date = self.today + relativedelta(days=+ day)
        name_day = calendar.day_name[dt.strptime(
            str(date.today()), '%Y-%m-%d').weekday()]

        if name_day == 'Saturday':
            end_date = timezone.now() + relativedelta(days=+ day)

        if name_day == 'Sunday':
            end_date = timezone.now() + relativedelta(days=+ day)
        return end_date

    def unblocked_date(self, devolution_date):
        if devolution_date:
            return self.today > devolution_date + relativedelta(days=+4)
        return False


def send_email(user, message):
    following_list = Following.objects.all().filter(user=user)
    user_list = [objuser.user.email for objuser in following_list]

    send_mail(
        subject="Biblioteka",
        message=message,
        recipient_list=user_list,
        from_email=settings.EMAIL_HOST_USER,
        fail_silently=False,
    )


def user_is_blocked(user, library):
    user = UserLibraryBlock.objects.filter(
        user=user, library=library).first()
    if user:
        return user.is_blocked
    return False


def unblocked_user(user, library):
    UserLibraryBlock.objects.get(
        user=user, library=library).delete()


def block_user(user, library):
    if not user_is_blocked(user, library):
        UserLibraryBlock.objects.create(
            user=user, library=library).save()

    UserLibraryBlock.objects.filter(
        user=user, library=library).update(is_blocked=Q(is_blocked=True))
