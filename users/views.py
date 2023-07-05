from rest_framework.views import Response
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import (
    IsAccountOwnerOrAdminOrEmployeeFollow,
    IsAdminOrEmployee,
    IsAccountOwnerOrAdminOrEmployee,
    IsAccountOwnerFollow,
)
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from libraries.models import LibraryEmployee
from .models import User
from django.shortcuts import get_object_or_404
from books.models import Following, Book, Rating
from books.serializers import FollowingSerializer, RatingSerializer


class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrEmployee]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserPostView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        is_superuser = serializer.validated_data.get("is_superuser")

        library_id = self.request.data.get("library_id")

        if is_superuser and library_id:
            library_data = get_object_or_404(LibraryEmployee, id=library_id)

            employeeUser = LibraryEmployee.objects.create(
                employee=user, library=library_data
            )

            employeeUser.save()


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminOrEmployee]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserFollowingBooksListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminOrEmployeeFollow]
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        books = []

        for book in serializer.data:
            books.append(book["book"])

        return Response(books)


class UserFollowingBooksCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerFollow]
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

    def perform_create(self, serializer):
        book_id_data = self.kwargs.get("pk")

        book = get_object_or_404(Book, id=book_id_data)

        try:
            follow_already_exists = Following.objects.get(
                user=self.request.user, book=book
            )
        except Following.DoesNotExist:
            follow_already_exists = None

        if follow_already_exists:
            raise ValidationError(
                {"message": "The user is already following this book"}
            )

        serializer.save(user=self.request.user, book=book)


class UserFollowingBooksDetailsView(generics.RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerFollow]
    queryset = Following.objects.all()
    serializer_class = FollowingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data["book"])


class UserRatingBookCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerFollow]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        rate = self.request.data.get("rating")

        description = self.request.data.get("description")

        book_id_data = self.kwargs.get("pk")

        book = get_object_or_404(Book, id=book_id_data)

        try:
            ratings_already_exists = Rating.objects.get(
                user=self.request.user, book=book
            )

        except Rating.DoesNotExist:
            ratings_already_exists = None

        if ratings_already_exists:
            raise ValidationError({"message": "The user already rated"})

        serializer.save(user=self.request.user, book=book)
