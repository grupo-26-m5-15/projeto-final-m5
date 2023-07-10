from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path("books/create/", views.BookCreateView.as_view()),
    path("books/", views.BookListView.as_view()),
    path("books/<int:pk>/", views.BookRetrieveView.as_view()),
    path("books/<int:pk>/", views.BookUpdateView.as_view()),
    path("books/<int:pk>/copies/", views.BookCopyListView.as_view()),
]
