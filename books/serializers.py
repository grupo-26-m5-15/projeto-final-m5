from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.serializers import UserSerializer
from .models import Book, Following, Rating
from copies.models import Copy
from copies.serializers import CopySerializer


class BookSerializer(serializers.ModelSerializer):
    copies = CopySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "type",
            "author",
            "synopsis",
            "release_date",
            "publishing_company",
            "add_at",
            "quantity",
            "copies",
        ]

        extra_kwargs = {
            "title": {"validators": [UniqueValidator(queryset=Book.objects.all())]}
        }

    def create(self, validated_data: dict) -> Book:
        book = Book.objects.create(**validated_data)
        Copy.objects.create(book=book)
        return book

    def get(self, validated_data: dict) -> Book:
        return Book.objects.all()

    def update(self, instance: Book, validated_data: dict) -> Book:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class FollowingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Following
        fields = ["id", "user", "book"]

    def create(self, validated_data: dict) -> Following:
        return Following.objects.create(**validated_data)

    def update(self, instance: Following, validated_data: dict) -> Following:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class FollowingSerializerGet(FollowingSerializer):
    user = UserSerializer(write_only=True)


class RatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)

    class Meta:
        model = Rating
        fields = ["id", "user", "book", "rating", "description"]

    def create(self, validated_data: dict) -> Rating:
        return Rating.objects.create(**validated_data)

    def update(self, instance: Rating, validated_data: dict) -> Rating:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class RatingSerializerGet(RatingSerializer):
    user = UserSerializer(write_only=True)
