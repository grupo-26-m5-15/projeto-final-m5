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
from .serializers import UserSerializer, UserAdminSerializer
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


class UserListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrEmployee]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @extend_schema(
        operation_id="list_users",
        responses={200: UserSerializer},
        description="List all users",
        summary="Only admin users or employess can list all users",
        tags=["List Users"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

    @extend_schema(
        operation_id="create_user",
        parameters=[
            UserSerializer,
            OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
            OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
        request=UserSerializer,
        responses={201: UserSerializer},
        description="Create users route",
        summary="Add personal informations to create a new user data",
        tags=["Create User"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class UserAdminView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer

    def perform_create(self, serializer):
        get_library_id = self.kwargs.get("pk")

        print(get_library_id)

        library = get_object_or_404(Library, pk=int(get_library_id))

        user = serializer.save()

        add_admin_in_library = LibraryEmployee.objects.create(
            employee=user, library=library
        )

        add_admin_in_library.save()

    @extend_schema(
        operation_id="create_admin",
        parameters=[
            UserAdminSerializer,
            OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
            OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
        request=UserAdminSerializer,
        responses={201: UserAdminSerializer},
        description="Create admin user route",
        summary="Add personal informations to create a new superuser data",
        tags=["Create Admin User"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


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

    @extend_schema(
        operation_id="get_user",
        responses={200: UserSerializer},
        description="Retrieve an user route",
        summary="Retrieve a specific user by cpf. Authenticated users, admin and employees can do this action.",
        tags=["Create Admin User"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="update_user",
        parameters=[
            UserSerializer,
            OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
            OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
        request=UserSerializer,
        responses={200: UserSerializer},
        description="Update an user route",
        summary="Update a specific user by cpf. Authenticated users, admin and employees can do this action.",
        tags=["Update User"],
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_user",
        description="Delete an user route",
        summary="Delete a specific user by cpf. Authenticated users, admin and employees can do this action.",
        tags=["Delete User"],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class UserFollowingBooksListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminOrEmployeeFollow]
    queryset = Following.objects.all()
    serializer_class = FollowingSerializerGet

    @extend_schema(
        operation_id="list_followings",
        responses={200: FollowingSerializerGet},
        description="List all user followings route",
        summary="List all user books following by cpf. Authenticated users, admin and employees can do this action.",
        tags=["List User Following Books"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

    @extend_schema(
        operation_id="create_follow",
        parameters=[
            FollowingSerializer,
            OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
            OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
        request=FollowingSerializer,
        responses={201: FollowingSerializer},
        description="Follow a book",
        summary="Create a follow by adding user and book instances",
        tags=["Create Follow"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    @extend_schema(
        operation_id="get_following_book",
        responses={200: FollowingSerializerGet},
        description="Retrive a specific user following book",
        summary="Retrieve a specific following book by its title.",
        tags=["Retrieve User Following Book"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_following_book",
        description="Delete a specific user following book",
        summary="Delete a specific following book by its title.",
        tags=["Delete User Following Book"],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class UserRatingBookCreateView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerFollow]
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    @extend_schema(
        operation_id="create_rating",
        parameters=[
            RatingSerializer,
            OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
            OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
        request=RatingSerializer,
        responses={201: RatingSerializer},
        description="Rate a book",
        summary="Create a rate by adding user and book instances and the rate",
        tags=["Create Rating"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    @extend_schema(
        operation_id="list_ratings",
        responses={200: RatingSerializerGet},
        description="List all user book ratings route",
        summary="List all user book ratings",
        tags=["List User Book Ratings"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

    @extend_schema(
        operation_id="retrieve_book_rating",
        responses={200: RatingSerializerGet},
        description="Retrieve a specific book rating route",
        summary="Retrieve a specific book rating by its title",
        tags=["Retrieve Book Rating"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="delete_book_rating",
        description="Delete a specific book rating route",
        summary="Delete a specific book rating by its title",
        tags=["Delete Book Rating"],
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


class HireALibrarianView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    queryset = LibraryEmployee.objects.all()
    serializer_class = LibraryEmployeeSerializer
    lookup_field = "cpf"

    @extend_schema(
        operation_id="hire_librarian",
        parameters=[
            LibraryEmployeeSerializer,
            OpenApiParameter("pk", OpenApiTypes.UUID, OpenApiParameter.PATH),
            OpenApiParameter("queryparam1", OpenApiTypes.UUID, OpenApiParameter.QUERY),
        ],
        request=LibraryEmployeeSerializer,
        responses={201: LibraryEmployeeSerializer},
        description="Hire a librarian route",
        summary="Hire a new employee by adding user and library instances",
        tags=["Hire Librarian"],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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

    @extend_schema(
        operation_id="retrieve_employee",
        responses={200: LibraryEmployeeSerializer},
        description="Retrieve a specific employee route",
        summary="Retrieve a specific employee by cpf",
        tags=["Retrieve Employee"],
    )
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @extend_schema(
        operation_id="fire_employee",
        responses={200: {"message": "employee fired with success"}},
        description="Fire a specific employee route",
        summary="Fire a specific employee by cpf",
        tags=["Fire Employee"],
    )
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

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


class ListAllUserLibraryBlocksView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAccountOwnerOrAdminOrEmployeeFollow]
    queryset = UserLibraryBlock.objects.all()
    serializer_class = UserLibraryBlockListSerializer
    lookup_field = "cpf"

    @extend_schema(
        operation_id="library_block_list",
        responses={200: UserLibraryBlockListSerializer},
        description="List all user blocked libraries route",
        summary="List all user blocked libraries",
        tags=["List User Blocked Libraries"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

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

    @extend_schema(
        operation_id="unblock_student",
        responses={200: {"message": "user unblocked with success"}},
        description="Unblock a student route",
        summary="Unblock a specific student by cpf",
        tags=["Unblock Student"],
    )
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

    @extend_schema(exclude=True)
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)


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

    @extend_schema(
        operation_id="user_loans_list",
        responses={200: ListLoanUserSerializer},
        description="List all user loans route",
        summary="List all user loans by cpf",
        tags=["List User Loans"],
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
