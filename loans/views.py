from rest_framework import generics

from .models import Loan
from .serializers import LoanSerializer
from rest_framework.pagination import PageNumberPagination
from users.permissions import IsAdminOrEmployee
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema


class LoanCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @extend_schema(
        parameters=["pk"],
        request=LoanSerializer,
        responses={201: LoanSerializer},
        description="Route to creating loans",
        summary="Only admin users or employess can create loans",
        tags=["Create Loans"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoanListView(generics.ListAPIView):
    pagination_class = PageNumberPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @extend_schema(
        responses={200: LoanSerializer},
        description="List all loans",
        summary="Only admin users or employess can list loans",
        tags=["List loans"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LoanRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    @extend_schema(
        responses={200: LoanSerializer},
        description="Retrieve loan by ID",
        summary="Only admin users or employess can retrieve loan",
        tags=["Retrieve loans"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        parameters=["pk"],
        responses={200: LoanSerializer},
        request=None,
        description="Route to return books",
        summary="Only admin users or employess can update loans",
        tags=["Update Loan"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
