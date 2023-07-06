from rest_framework import serializers
from django.shortcuts import get_object_or_404
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator

from .models import Copy


class CopySerializer(serializers.ModelSerializer):
    class Meta:
        model = Copy
        fields = ["id", "book", "is_available"]
