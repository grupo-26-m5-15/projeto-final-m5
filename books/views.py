from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateAPIView,
    ListCreateAPIView,
)
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

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

    @extend_schema(
        parameters=[BookSerializer],
        responses={200, BookSerializer},
        operation_id="create_book",
        description="Create a new book",
        summary="Route to create a new book",
        tags=["Books"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class BookListView(ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("id")

    @extend_schema(
        operation_id="create_book",
        description="List all books",
        summary="Route to list all book",
        tags=["Books"],
    )
    def get(self, request):
        return self.list(request)


class BookRetrieveUpdateView(RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    serializer_class = BookSerializer
    queryset = Book.objects.all().order_by("id")

    @extend_schema(
        operation_id="list_all_book",
        description="Retrieve a book by ID",
        summary="Route to retrieve a book by ID",
        tags=["Books"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="update_book",
        description="Update a book by ID",
        summary="Route to update a book by ID",
        tags=["Books"],
    )
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class BookCopyListView(ListAPIView):
    serializer_class = CopySerializer

    @extend_schema(
        operation_id="list_copy_book",
        description="List the copies of a book searching by its ID",
        summary="List the copies of a book",
        tags=["Books"],
    )
    def get_queryset(self):
        book = get_object_or_404(Book, pk=self.kwargs.get("pk"))

        return Copy.objects.filter(book=book)
