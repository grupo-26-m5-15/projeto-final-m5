from django.urls import path
from . import views
from .views import (
    UserListView,
    UserPostView,
    UserDetailsView,
    UserFollowingBooksListView,
    UserFollowingBooksDetailsView,
    UserFollowingBooksCreateView,
)

from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("users/", UserListView.as_view()),
    path("users/create/", UserPostView.as_view()),
    path("users/<int:pk>/", UserDetailsView.as_view()),
    path("login/", jwt_views.TokenObtainPairView.as_view()),
    path("users/books/following/", UserFollowingBooksListView.as_view()),
    path("users/book/<int:pk>/follow/", UserFollowingBooksCreateView.as_view()),
    path(
        "users/book/<int:pk>/read_or_unfollow/", UserFollowingBooksDetailsView.as_view()
    ),
]
