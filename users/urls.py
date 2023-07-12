from django.urls import path

from .views import (
    UserListView,
    UserPostView,
    UserAdminView,
    UserDetailsView,
    UserFollowingBooksListView,
    UserFollowingBooksDetailsView,
    UserFollowingBooksCreateView,
    UserRatingBookCreateView,
    UserRatingBooksListView,
    UserRatingBookDetailsView,
    HireALibrarianView,
    RetrieveOrFireEmployeeView,
    ListAllUserLibraryBlocksView,
    UnblockStudentView,
    ListLoanUserViews,
)

from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path("users/", UserListView.as_view()),
    path("users/create/", UserPostView.as_view()),
    path("users/<int:pk>/create_admin/", UserAdminView.as_view()),
    path("users/<str:cpf>/", UserDetailsView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("users/books/following/", UserFollowingBooksListView.as_view()),
    path("users/book/<int:pk>/follow/", UserFollowingBooksCreateView.as_view()),
    path(
        "users/book/<str:title>/read_or_unfollow/",
        UserFollowingBooksDetailsView.as_view(),
    ),
    path("users/book/<int:pk>/rate/", UserRatingBookCreateView.as_view()),
    path("users/books/rating/", UserRatingBooksListView.as_view()),
    path(
        "users/book/<str:title>/read_or_delete_rate/",
        UserRatingBookDetailsView.as_view(),
    ),
    path("users/library/<str:cpf>/employee/", HireALibrarianView.as_view()),
    path(
        "users/library/<str:cpf>/retrieve_or_fire_employee/",
        RetrieveOrFireEmployeeView.as_view(),
    ),
    path("users/<str:cpf>/library_blocks", ListAllUserLibraryBlocksView.as_view()),
    path("users/<str:cpf>/unblock", UnblockStudentView.as_view()),
    path("users/<str:cpf>/loans", ListLoanUserViews.as_view()),
]
