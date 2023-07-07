from django.urls import path
from . import views


urlpatterns = [
    path("loans/", views.LoanListView.as_view()),
    path("books/<int:pk>/loans/", views.LoanCreateView.as_view()),
    path("loans/<int:pk>/users/", views.LoanRetrieveView.as_view()),
]
