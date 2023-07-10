from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.fields import ReadOnlyField
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "cpf",
            "username",
            "password",
            "is_superuser",
            "image",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": [UniqueValidator(queryset=User.objects.all())]},
            "is_superuser": {"read_only": True},
        }

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")

        if request and request.method != "POST":
            fields["is_superuser"] = ReadOnlyField()

        return fields

    def create(self, validated_data: dict) -> User:
        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)

            else:
                setattr(instance, key, value)

        instance.save()

        return instance


class UserAdminSerializer(UserSerializer):
    def create(self, validated_data: dict) -> User:
        return User.objects.create_superuser(**validated_data)
