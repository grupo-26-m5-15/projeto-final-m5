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

from drf_spectacular.utils import extend_schema


class ListLibraryView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    @extend_schema(
        operation_id="list_library",
        responses={200: LibrarySerializer},
        description="List all libraries",
        summary="Only admin users or employess can list all libraries",
        tags=["List All Library"],
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CreateLibraryView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    @extend_schema(
        operation_id="create_library",
        responses={201: LibrarySerializer},
        description="Create a library",
        summary="Only general manager can create libraries",
        tags=["Create Library"],
    )
    def post(self, req, *args, **kwargs):
        return self.create(req, *args, **kwargs)


class LibraryDetailViews(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    @extend_schema(
        operation_id="Retrive_library",
        responses={200: LibrarySerializer},
        description="List library by ID",
        summary="Only admins and employees can list your libraries",
        tags=["List library"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        operation_id="Update_library",
        responses={200: LibrarySerializer},
        description="Update library information",
        summary="Only admins can update library informations",
        tags=["Update library"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(
        operation_id="Destroy_library",
        responses={201: None},
        description="Delete library by ID",
        summary="Only general manager can destroy library",
        tags=["Destroy library"],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class ListLibraryBooks(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        library = get_object_or_404(Library, pk=self.kwargs.get("pk"))
        queryset = Book.objects.filter(library=library)
        return queryset

    @extend_schema(
        operation_id="List_Library_books",
        responses={200: BookSerializer},
        description="List library book",
        summary="Only authenticated users can list books from a specific library",
        tags=["List library books"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListLibraryEmployees(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Book.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        library = get_object_or_404(Library, pk=self.kwargs.get("pk"))
        queryset = User.objects.filter(library=library)
        return queryset

    @extend_schema(
        operation_id="List_library_employees",
        responses={200: UserSerializer},
        description="List library employees",
        summary="Only authenticated users can list employees from a specific library",
        tags=["List library employees"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListLibraryLoans(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def get_queryset(self):
        library = get_object_or_404(Library, pk=self.kwargs.get("pk"))
        queryset = Loan.objects.filter(library=library)
        return queryset

    @extend_schema(
        operation_id="List_library_loans",
        responses={200: LoanSerializer},
        description="List library loans",
        summary="Only administrators and employees can list your library's loans",
        tags=["List library loans"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ListLibraryUsersBlocked(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = UserLibraryBlock
    serializer_class = UserLibraryBlockListSerializer

    def get_queryset(self):
        library = get_object_or_404(Library, pk=self.kwargs.get("pk"))
        queryset = UserLibraryBlock.objects.filter(library=library)
        return queryset

    @extend_schema(
        operation_id="List_library_users_blocked",
        responses={200: UserSerializer},
        description="Lists all users that are locked in the library",
        summary="Only adminstrators and employees can list your library's users blocked",
        tags=["List library users blocked"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
