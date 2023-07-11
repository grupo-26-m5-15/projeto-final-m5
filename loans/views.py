# from django.shortcuts import render
from rest_framework import generics

from .models import Loan
from .serializers import LoanSerializer
from rest_framework.pagination import PageNumberPagination
from users.permissions import IsAdminOrEmployee


class LoanCreateView(generics.CreateAPIView):
    # permission_classes = [IsAdminOrEmployee]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanListView(generics.ListAPIView):
    pagination_class = PageNumberPagination

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdminOrEmployee]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
