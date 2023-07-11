from rest_framework import serializers
from .models import Loan
from users.models import User
from libraries.models import Library
from copies.models import Copy
from books.models import Book, Following
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from users.serializers import UserSerializer
from .utils import Dates, user_is_blocked, block_user, send_email, unblocked_user
from libraries.serializers import LibrarySerializer
from copies.serializers import CopySerializer


class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    library = LibrarySerializer(read_only=True)
    copy = CopySerializer(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "start_date",
            "end_date",
            "devolution_date",
            "library",
            "user",
            "copy",
        ]
        depth = 1
        extra_kwargs = {
            "start_date": {"read_only": True},
            "copy": {"read_only": True},
        }

    def create(self, validated_data: dict) -> Loan:

        request = self.context["request"].data
        copy_id = self.context["view"].kwargs["pk"]
        user = get_object_or_404(User, pk=request["user_id"])
        library = get_object_or_404(Library, pk=request["library_id"])
        copy = get_object_or_404(Copy, pk=copy_id)

        book = Book.objects.get(pk=copy.book_id)
        follow = Following.objects.all().filter(book=book)
        loan_list = Loan.objects.all().filter(user_id=request["user_id"])

        today = Dates().today
        for loan in loan_list:
            if user_is_blocked(user, library):
                if Dates().unblocked_date(loan.devolution_date):
                    unblocked_user(user, library)
                raise serializers.ValidationError(
                    {"Error": "User Blocked haha"}
                )

            if today > loan.end_date and loan.devolution_date == None:
                block_user(user, library)
                raise serializers.ValidationError(
                    {"Error": "User Blocked HOHO"})

        if copy.is_available is False or book.quantity < 1:
            raise serializers.ValidationError(
                {"Error": "Copy not Currently unavailable"})

        payload = {
            "end_date": str(Dates().devolution_date(10))
            if len(follow) >= 10 < 20
            else str(Dates().devolution_date(7))
            if len(follow) >= 20
            else str(Dates().devolution_date(15)),
            "user_id": request["user_id"],
            "copy_id": copy_id,
            "library_id": request["library_id"],
        }

        Book.objects.filter(pk=copy.book_id).update(quantity=F("quantity") - 1)
        created = Loan.objects.create(**payload)

        book = Book.objects.get(pk=copy.book_id)

        if book.quantity < 1:
            send_email(user, f"The book {book.title} currently available")
            Copy.objects.filter(book=book).update(
                is_available=Q(is_available=False))

        return created

    def update(self, instance: Loan, validated_data: dict) -> Loan:
        if instance.devolution_date is not None:
            raise serializers.ValidationError(
                {"Error": "Copy has already been returned"}
            )

        for key, value in {"devolution_date": str(Dates().today)}.items():
            setattr(instance, key, value)

        book = Book.objects.filter(pk=instance.copy.book_id)
        book.update(quantity=F("quantity") + 1)

        if book.first().quantity == 1:
            send_email(instance.user,
                       f"The book, {book.first().title} is available")
            Copy.objects.filter(book=book.first()).update(
                is_available=Q(is_available=True))

        instance.save()
        return instance


class ListLoanUserSerializer(LoanSerializer):
    user = UserSerializer(write_only=True)
