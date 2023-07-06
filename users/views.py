from rest_framework import generics
from rest_framework.views import Response, status
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import (
    IsAccountOwnerOrAdminOrEmployeeFollow,
    IsAdminOrEmployee,
    IsAccountOwnerOrAdminOrEmployee,
    IsAccountOwnerFollow,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserSerializer
from loans.models import Loan
from loans.serializers import ListLoanUserSerializer
from libraries.models import LibraryEmployee, Library, UserLibraryBlock
from libraries.serializers import LibraryEmployeeSerializer, UserLibraryBlockSerializer
from .models import User
from django.shortcuts import get_object_or_404
from books.models import Following, Book, Rating
from books.serializers import (
    FollowingSerializer,
    RatingSerializer,
    RatingSerializerGet,
    FollowingSerializerGet,
)


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

        library_id = int(self.request.data.get("library_id"))

        if is_superuser and library_id:
            library_data = get_object_or_404(Library, id=library_id)

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
    serializer_class = FollowingSerializerGet


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
    serializer_class = FollowingSerializerGet


class UserRatingBookCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerFollow]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def perform_create(self, serializer):
        book_id_data = self.kwargs.get("pk")

        book = get_object_or_404(Book, id=book_id_data)

        try:
            ratings_already_exists = Rating.objects.get(
                user=self.request.user, book=book
            )

        except Rating.DoesNotExist:
            ratings_already_exists = None

        if ratings_already_exists:
            raise ValidationError({"message": "The user already rated this book"})

        serializer.save(user=self.request.user, book=book)


class UserRatingBooksListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminOrEmployeeFollow]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializerGet


class UserRatingBookDetailsView(generics.RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerFollow]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializerGet


class HireALibrarianView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = LibraryEmployee.objects.all()
    serializer_class = LibraryEmployeeSerializer

    def perform_create(self, serializer):
        user_id = self.kwargs.get("pk")

        user = get_object_or_404(User, id=user_id)

        get_library_admin = LibraryEmployee.objects.filter(
            employee=self.request.user
        ).first()

        library = get_library_admin.library if get_library_admin else None

        try:
            user_already_hired = LibraryEmployee.objects.get(
                employee=user, is_employee=True
            )

        except LibraryEmployee.DoesNotExist:
            user_already_hired = None

        if user_already_hired and user_already_hired.is_employee:
            raise ValidationError({"message": "This user is already an employee"})

        serializer.save(employee=user, library=library)


class RetrieveOrFireEmployeeView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = LibraryEmployee.objects.all()
    serializer_class = LibraryEmployeeSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        user = get_object_or_404(User, pk=self.kwargs[lookup_url_kwarg])

        library_employee = get_object_or_404(
            LibraryEmployee, employee=user, is_employee=True
        )

        self.check_object_permissions(self.request, library_employee)

        return library_employee

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        instance.is_employee = False
        instance.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": "employee fired with success"}, status=status.HTTP_200_OK
        )


class ListAllUserLibraryBlocksView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminOrEmployeeFollow]
    queryset = UserLibraryBlock.objects.all()
    serializer_class = UserLibraryBlockSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        queryset = UserLibraryBlock.objects.filter(user=user, is_blocked=True)
        return queryset


class UnblockStudentView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrEmployee]
    queryset = UserLibraryBlock.objects.all()
    serializer_class = UserLibraryBlockSerializer

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        user = get_object_or_404(User, pk=self.kwargs[lookup_url_kwarg])

        library_employee = get_object_or_404(
            LibraryEmployee, employee=self.request.user, is_employee=True
        )

        library = library_employee.library if library_employee else None

        user_blocked = get_object_or_404(
            UserLibraryBlock, user=user, library=library, is_blocked=True
        )

        self.check_object_permissions(self.request, user_blocked)

        return user_blocked

    def patch(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        instance.is_blocked = False
        instance.save()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": "user unblocked with success"}, status=status.HTTP_200_OK
        )


class ListLoanUserViews(generics):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminOrEmployeeFollow]
    queryset = Loan.objects.all()
    serializer_class = ListLoanUserSerializer

    def get_queryset(self):
        user = get_object_or_404(User, pk=self.kwargs["pk"])
        queryset = Loan.objects.filter(user=user)
        return queryset
