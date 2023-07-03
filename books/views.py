from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView

from .models import Book
from .serializers import BookSerializer


class BookView(ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [custom_permission]

    serializer_class = BookSerializer
    queryset = Book.objects.all()


class BookRetrieveUpdateDeleteView(RetrieveUpdateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [custom_permission]

    queryset = Book.objects.all()
    serializer_class = BookSerializer
