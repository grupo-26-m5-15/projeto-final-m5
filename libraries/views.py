from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import User
from users.serializers import UserSerializer
from users.permissions import IsAdminOrEmployee

from books.models import Book
from books.serializers import BookSerializer

from loans.models import Loan
from loans.serializers import LoanSerializer

from .models import Library, UserLibraryBlock
from .serializers import (
    LibrarySerializer,
    UserLibraryBlockListSerializer,
)


class ListLibraryView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer


class CreateLibraryView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer


class LibraryDetailViews(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer


class ListLibraryBooks(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        library = get_object_or_404(Library, pk=self.kwargs.get("pk"))
        queryset = Book.objects.filter(library=library)
        return queryset


class ListLibraryEmployees(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Book.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        library = get_object_or_404(Library, pk=self.kwargs.get("pk"))
        queryset = User.objects.filter(library=library)
        return queryset


class ListLibraryLoans(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_queryset(self):
        library = get_object_or_404(Library, pk=self.kwargs.get("pk"))
        queryset = Loan.objects.filter(library=library)
        return queryset


class ListLibraryUsersBlocked(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = UserLibraryBlock
    serializer_class = UserLibraryBlockListSerializer

    def get_queryset(self):
        library = get_object_or_404(Library, pk=self.kwargs.get("pk"))
        queryset = UserLibraryBlock.objects.filter(library=library)
        return queryset
