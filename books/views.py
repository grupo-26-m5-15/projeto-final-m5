from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from django.shortcuts import get_object_or_404

from .models import Book
from .serializers import BookSerializer
from copies.models import Copy
from copies.serializers import CopySerializer


class BookView(ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [custom_permission]

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("id")


class BookRetrieveUpdateDeleteView(RetrieveUpdateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [custom_permission]

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("id")


class BookCopyListCreateView(ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [custom_permission]

    serializer_class = CopySerializer
    queryset = Copy.objects.all().order_by("id")
