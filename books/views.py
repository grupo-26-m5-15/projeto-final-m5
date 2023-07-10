from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    ListCreateAPIView,
)
from django.shortcuts import get_object_or_404

from .models import Book
from .serializers import BookSerializer
from copies.models import Copy
from copies.serializers import CopySerializer
from users.permissions import IsAdminOrEmployee


class BookCreateView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("id")


class BookListView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("id")


class BookRetrieveView(RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.get_queryset()


class BookUpdateView(UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("id")


class BookCopyListView(ListAPIView):
    serializer_class = CopySerializer

    def get_queryset(self):
        book = get_object_or_404(Book, pk=self.kwargs.get("pk"))

        return Copy.objects.filter(book=book)
