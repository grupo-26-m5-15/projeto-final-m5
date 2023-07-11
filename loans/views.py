from rest_framework import generics

from .models import Loan
from .serializers import LoanSerializer
from rest_framework.pagination import PageNumberPagination
from users.permissions import IsAdminOrEmployee
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


class LoanCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanListView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanRetrieveView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
