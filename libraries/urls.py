from django.urls import path
from .views import ListLibraryView, CreateLibraryView, LibraryDetailViews, ListLibraryBooks, ListLibraryEmployees, ListLibraryLoans
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("libraries/", ListLibraryView.as_view()),
    path("libraries/create/", CreateLibraryView.as_view()),
    path("libraries/<int:pk>/", LibraryDetailViews.as_view()),
    path("libraries/<int:pk>/books/", ListLibraryBooks.as_view()),
    path("libraries/<int:pk>/employees/", ListLibraryEmployees.as_view()),
    path("libraries/<int:pk>/loans/", ListLibraryLoans.as_view())
]
