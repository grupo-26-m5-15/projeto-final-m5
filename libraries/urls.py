from django.urls import path
from .views import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("libraries/", views.LibraryViews.as_views()),
    path("libraries/<int:pk>", views.LibraryDetailViews.as_views()),
    path("libraries/<int:pk>/books/", views.LibraryRetrieverBookViews.as_views()),
]
