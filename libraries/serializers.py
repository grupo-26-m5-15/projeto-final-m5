from rest_framework import serializers

from .models import Library, LibraryBooks, LibraryEmployee, UserLibraryBlock


class LibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = [
            "id",
            "name",
            "cnpj",
            "email",
            "address",
        ]

    def create(self, validated_data):
        return Library.objects.create(**validated_data)
