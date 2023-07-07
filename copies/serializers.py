from rest_framework import serializers
from .models import Copy
from books.serializers import BookSerializer


class CopySerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Copy
        fields = ["id", "book", "is_available"]

    def create(self, validated_data: dict) -> Copy:
        return Copy.objects.create(**validated_data)

    def update(self, instance: Copy, validated_data: dict) -> Copy:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
