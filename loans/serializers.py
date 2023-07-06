from rest_framework import serializers

from copies.serializers import CopySerializer
from users.serializers import UserSerializer

from .models import Loan


class LoanSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    copy = CopySerializer(read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "start_date",
            "end_date",
            "devolution_date",
            "user",
            "copy"
             ]

    def create(self, validated_data: dict) -> Loan:
        return Loan.objects.create(**validated_data)

    def update(self, instance: Loan, validated_data: dict) -> Loan:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance


class ListLoanUserSerializer(LoanSerializer):
    user = UserSerializer(write_only=True)
