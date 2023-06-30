from rest_framework import serializers
from .models import Book
from rest_framework.validators import UniqueValidator


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "type", "author", "release_date", "publishing_company"]

        extra_kwargs = {
            "title": {"validators": [UniqueValidator(queryset=Book.objects.all())]}
        }

    def create(self, validated_data: dict) -> Book:
        return Book.objects.create(**validated_data)
