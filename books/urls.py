from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views
from copies.views import CopyView


urlpatterns = [
    path("books/", views.BookView.as_view()),
    path("books/<int:pk>/", views.BookRetrieveUpdateDeleteView.as_view()),
    path("books/<int:pk>/copies/", CopyView.as_view()),
]
