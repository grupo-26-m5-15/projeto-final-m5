from rest_framework import serializers
from .models import Loan
from users.models import User
from libraries.models import Library, UserLibraryBlock
from copies.models import Copy
from books.models import Book, Following
from django.shortcuts import get_object_or_404
from django.db.models import F, Q
from users.serializers import UserSerializer
from .utils import Dates
class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "id",
            "start_date",
            "end_date",
            "devolution_date",
            "library",
            "user",
            "copy"
        ]
        depth = 1
        extra_kwargs = {
            "start_date": {"read_only": True},
            "copy": {"read_only": True},
        }
    def create(self, validated_data: dict) -> Loan:
        request = self.context['request'].data
        copy_id = self.context['view'].kwargs['pk']
        user = get_object_or_404(User, pk=request["user_id"])
        library = get_object_or_404(Library, pk=request["library_id"])
        copy = get_object_or_404(Copy, pk=copy_id)
        loan_list = Loan.objects.all().filter(user_id=request["user_id"])
        today = Dates().today
        for loan in loan_list:
            if today > loan.end_date and loan.devolution_date == None:
                UserLibraryBlock.objects.create(
                    user=user, library=library).save()
                raise serializers.ValidationError(
                    {"Error": "Devolve logo o que vc pegou! :-P "})
        if copy.is_available is False:
            raise serializers.ValidationError(
                {"Error": "Currently unavailable"})
        book = Book.objects.get(pk=copy.book_id)
        follow = Following.objects.all().filter(book=book)
        book_quantity = book.quantity
        if book_quantity < 1:
            Copy.objects.filter(book=book).update(
                is_available=Q(is_available=False))
            raise serializers.ValidationError(
                {"Error": "Copy not currently available"})
        payload = {
            "end_date": str(Dates().devolution_date(10)) if len(follow) >= 10 < 20 else str(Dates().devolution_date(7)) if len(follow) >= 20 else str(Dates().devolution_date(15)),
            "user_id": request["user_id"],
            "copy_id": copy_id,
            "library_id": request["library_id"]
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
class ListLoanUserSerializer(LoanSerializer):
    user = UserSerializer(write_only=True)
