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

from libraries.models import LibraryBooks, LibraryEmployee

from .models import Book
from .serializers import BookSerializer
from copies.models import Copy
from copies.serializers import CopySerializer
from users.permissions import IsAdminOrEmployee, SafeAccess
from libraries.serializers import LibraryBooksSerializer, Library
from rest_framework.exceptions import ValidationError


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
    permission_classes = [SafeAccess]

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


class BookLibraryCreate(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]
    queryset = LibraryBooksSerializer.objects.all()
    serializer_class = LibraryBooksSerializer
    lookup_field = "title"

    def perform_create(self, serializer):
        book_title = self.kwargs.get("title")

        book = get_object_or_404(Book, title=book_title)

        try:
            get_library_admin = LibraryEmployee.objects.filter(
                employee=self.request.user
            ).first()
        except LibraryEmployee.DoesNotExist:
            raise ValidationError({"message": "Admin to this library was not found"})

        library = get_library_admin.library if get_library_admin else None

        try:
            book_library = LibraryBooks.objects.get(book=book, library=library)

        except LibraryEmployee.DoesNotExist:
            book_library = None

        if book_library:
            raise ValidationError(
                {"message": "This book was already added to this library"}
            )

        serializer.save(book=book, library=library)

    @extend_schema(
        operation_id="create_library_book",
        description="Add a specific book to a library by its title",
        summary="Add book to a library",
        tags=["Books"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
