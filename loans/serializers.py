from rest_framework import serializers
from .models import Loan
from users.models import User
from copies.models import Copy
from books.models import Book
import calendar
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from django.shortcuts import get_object_or_404
from django.db.models import F
from copies.serializers import CopySerializer
from users.serializers import UserSerializer


def devolution_date():
    end_date = date.today() + relativedelta(days=+15)
    name_day = calendar.day_name[datetime.datetime.strptime(
        str(end_date), '%Y-%m-%d').weekday()]

    if name_day == 'Saturday':
        end_date = date.today() + relativedelta(days=+17)

    if name_day == 'Sunday':
        end_date = date.today() + relativedelta(days=+16)
    return end_date


class LoanSerializer(serializers.ModelSerializer):
    # copy = CopySerializer(read_only=True)
    # user_id = UserSerializer(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "start_date",
            "end_date",
            "devolution_date",
            "user_id",
            "copy"
        ]
        extra_kwargs = {
            "start_date": {"read_only": True},
            "copy": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Loan:

        user_id = self.context['request'].data
        copy_id = self.context['view'].kwargs['pk']

        get_object_or_404(User, pk=user_id["user_id"])
        copy = get_object_or_404(Copy, pk=copy_id)

        if copy.availability is False:
            raise serializers.ValidationError(
                {"Error": "Currently unavailable"})

        book = Book.objects.get(pk=copy.book_id)
        book_availability = book.quantity

        if book_availability < 1:
            Copy.objects.filter(pk=copy.book_id).update(
                quantity=F('quantity') - 1)
            raise serializers.ValidationError(
                {"Error": "Copy not currently available"})

        payload = {
            "end_date": str(devolution_date()),
            "user_id": user_id["user_id"],
            "copy_id": copy_id,
        }

        Book.objects.filter(pk=copy.book_id).update(quantity=F('quantity') - 1)

        return Loan.objects.create(**payload)

    def update(self, instance: Loan, validated_data: dict) -> Loan:

        if instance.devolution_date is not None:
            raise serializers.ValidationError(
                {"Error": "Copy has already been returned"})

        copy = Copy.objects.get(pk=instance.copy_id)
        Book.objects.filter(pk=copy.book_id).update(quantity=F('quantity') + 1)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
