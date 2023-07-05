from django.urls import path

from . import views

# from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("loans/", views.LoanListCreateView.as_view()),
    path("loans/<int:pk>/users", views.LoanRetrieveView.as_view()),
]
