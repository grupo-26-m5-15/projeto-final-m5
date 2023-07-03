from django.urls import path
from . import views

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<int:pk>/", views.BookRetrieveUpdateDeleteView.as_view()),
]
