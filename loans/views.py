# from django.shortcuts import render
from rest_framework import generics

from .models import Loan
from .serializers import LoanSerializer

# from rest_framework.permissions import (IsAdminUser, IsAuthenticated,
#                                         IsAuthenticatedOrReadOnly)
# from rest_framework_simplejwt.authentication import JWTAuthentication


class LoanListCreateView(generics.ListCreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanRetrieveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
