# from rest_framework import serializers
# from .models import Loan
# from users.models import User
# from libraries.models import Library
# from copies.models import Copy
# from books.models import Book, Following
# from django.shortcuts import get_object_or_404
# from django.db.models import F
# from users.serializers import UserSerializer

import calendar
from datetime import date, datetime as dt
from dateutil.relativedelta import relativedelta
from django.utils import timezone


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


def books_request():
    ...


def followings_request():
    ...


def users_request():
    ...


def copies_request():
    ...


def libraries_request():
    ...
