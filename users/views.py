from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
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
from .serializers import (
    UserSerializer,
    UserAdminSerializer,
    EmailTokenObtainPairSerializer,
)
from loans.models import Loan
from loans.serializers import ListLoanUserSerializer
from libraries.models import LibraryEmployee, Library, UserLibraryBlock
from libraries.serializers import (
    LibraryEmployeeSerializer,
    UserLibraryBlockSerializer,
    UserLibraryBlockListSerializer,
)
from .models import User
from django.shortcuts import get_object_or_404
from books.models import Following, Book, Rating
from books.serializers import (
    FollowingSerializer,
    RatingSerializer,
    RatingSerializerGet,
    FollowingSerializerGet,
)
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrEmployee]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        first_name = self.request.query_params.get("first_name")
        email = self.request.query_params.get("email")
        username = self.request.query_params.get("username")
        cpf = self.request.query_params.get("cpf")

        queryset = super().get_queryset()

        if first_name:
            queryset = queryset.filter(first_name__istartswith=first_name)

        if email:
            queryset = queryset.filter(email__icontains=email)

        if cpf:
            queryset = queryset.filter(cpf__contains=cpf)

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset


class UserPostView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserAdminView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        get_library_id = self.kwargs.get("pk")

        library = get_object_or_404(Library, pk=int(get_library_id))

        add_admin_in_library = LibraryEmployee.objects.create(
            employee=user, library=library
        )

        add_admin_in_library.save()


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminOrEmployee]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "cpf"

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        user_cpf = self.kwargs[lookup_url_kwarg]

        user = get_object_or_404(User, cpf=user_cpf)

        self.check_object_permissions(self.request, user)

        return user

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class UserFollowingBooksListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminOrEmployeeFollow]
    queryset = Following.objects.all()
    serializer_class = FollowingSerializerGet

    def get_queryset(self):
        title = self.request.query_params.get("title")
        type = self.request.query_params.get("type")
        author = self.request.query_params.get("author")
        publishing_company = self.request.query_params.get("publishing_company")

        queryset = super().get_queryset()

        if title:
            queryset = queryset.filter(book__title__istartswith=title)

        if type:
            queryset = queryset.filter(book__type__icontains=type)

        if author:
            queryset = queryset.filter(book__author__istartswith=author)

        if publishing_company:
            queryset = queryset.filter(
                book__publishing_company__istartswith=publishing_company
            )

        return queryset


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
    lookup_field = "title"

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        book_title = self.kwargs[lookup_url_kwarg]

        book = get_object_or_404(Book, title__istartswith=book_title)

        following = get_object_or_404(Following, book=book)

        self.check_object_permissions(self.request, following)

        return following

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


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

    def get_queryset(self):
        title = self.request.query_params.get("title")
        type = self.request.query_params.get("type")
        author = self.request.query_params.get("author")
        publishing_company = self.request.query_params.get("publishing_company")

        queryset = super().get_queryset()

        if title:
            queryset = queryset.filter(book__title__istartswith=title)

        if type:
            queryset = queryset.filter(book__type__icontains=type)

        if author:
            queryset = queryset.filter(book__author__istartswith=author)

        if publishing_company:
            queryset = queryset.filter(
                book__publishing_company__istartswith=publishing_company
            )

        return queryset


class UserRatingBookDetailsView(generics.RetrieveDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerFollow]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializerGet
    lookup_field = "title"

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        book_title = self.kwargs[lookup_url_kwarg]

        book = get_object_or_404(Book, title__istartswith=book_title)

        following = get_object_or_404(Rating, book=book)

        self.check_object_permissions(self.request, following)

        return following

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class HireALibrarianView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = LibraryEmployee.objects.all()
    serializer_class = LibraryEmployeeSerializer
    lookup_field = "cpf"

    def perform_create(self, serializer):
        user_cpf = self.kwargs.get("cpf")

        user = get_object_or_404(User, cpf=user_cpf)

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
    lookup_field = "cpf"

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        user = get_object_or_404(User, cpf=self.kwargs[lookup_url_kwarg])

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
    serializer_class = UserLibraryBlockListSerializer
    lookup_field = "cpf"

    def get_queryset(self):
        user = get_object_or_404(User, cpf=self.kwargs["cpf"])
        queryset = UserLibraryBlock.objects.filter(user=user, is_blocked=True)
        return queryset


class UnblockStudentView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrEmployee]
    queryset = UserLibraryBlock.objects.all()
    serializer_class = UserLibraryBlockSerializer
    lookup_field = "cpf"

    def get_object(self):
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            "Expected view %s to be called with a URL keyword argument "
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            "attribute on the view correctly."
            % (self.__class__.__name__, lookup_url_kwarg)
        )

        user = get_object_or_404(User, cpf=self.kwargs[lookup_url_kwarg])

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


class ListLoanUserViews(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminOrEmployeeFollow]
    queryset = Loan.objects.all()
    serializer_class = ListLoanUserSerializer
    lookup_field = "cpf"

    def get_queryset(self):
        user = get_object_or_404(User, cpf=self.kwargs["cpf"])
        queryset = Loan.objects.filter(user=user)

        return queryset
