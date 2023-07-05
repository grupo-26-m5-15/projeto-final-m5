from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import Copy
from books.models import Book
from books.serializers import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ["id", "book", "is_available"]

        # extra_kwargs = {
        #     "name": {
        #         "validators": [UniqueValidator(queryset=YourModelName.objects.all())]
        #     }
        # }
