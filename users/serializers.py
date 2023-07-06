from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.fields import ReadOnlyField
from .models import User
from libraries.models import Library


class UserSerializer(serializers.ModelSerializer):

    library_id = serializers.SerializerMethodField()

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
            "library_id",
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {"validators": [UniqueValidator(queryset=User.objects.all())]},
        }

    def get_library_id(self, obj):
        request = self.context.get("request")

        library_id_value = request.data.get("library_id")

        if library_id_value:
            return library_id_value

        return None

    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get("request")

        if request and request.method != "POST":
            fields["is_superuser"] = ReadOnlyField()

        return fields

    def create(self, validated_data: dict) -> User:
        superuser = validated_data.get("is_superuser")
        if superuser:
            return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)

            else:
                setattr(instance, key, value)

        instance.save()

        return instance
