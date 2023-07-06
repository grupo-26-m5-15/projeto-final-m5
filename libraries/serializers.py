from rest_framework import serializers

from .models import Library, LibraryBooks, LibraryEmployee, UserLibraryBlock
from users.serializers import UserSerializer
from books.serializers import BookSerializer


class LibrarySerializer(serializers.ModelSerializer):

    employees = UserSerializer(read_only=True, many=True)
    books = BookSerializer(read_only=True, many=True)

    class Meta:
        model = Library
        fields = [
            "id",
            "name",
            "cnpj",
            "email",
            "address",
            "employees"
        ]

    def create(self, validated_data):
        return Library.objects.create(**validated_data)

    def update(self, instance: Library, validated_data: dict) -> Library:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class LibraryEmployeeSerializer(serializers.ModelSerializer):
    library = LibrarySerializer(read_only=True)
    employee = UserSerializer(read_only=True)

    class Meta:
        model = LibraryEmployee
        fields = ["id", "library", "employee", "is_employee"]

    def create(self, validated_data):
        return Library.objects.create(**validated_data)

    def update(self, instance: Library, validated_data: dict) -> Library:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class LibraryBooksSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    library = LibrarySerializer(read_only=True)

    class Meta:
        model = LibraryBooks
        fields = ["id", "book", "library"]

    def create(self, validated_data):
        return LibraryBooks.objects.create(**validated_data)

    def update(self, instance: LibraryBooks, validated_data: dict) -> LibraryBooks:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class UserLibraryBlockSerializer(serializers.ModelSerializer):
    library = LibrarySerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserLibraryBlock
        fields = ["id", "library", "user", "is_blocked"]

    def create(self, validated_data):
        return UserLibraryBlock.objects.create(**validated_data)

    def update(
        self, instance: UserLibraryBlock, validated_data: dict
    ) -> UserLibraryBlock:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
