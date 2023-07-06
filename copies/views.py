# from rest_framework.views import APIView, Request, Response, status
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView, Request, Response, status

from .models import Copy
from .serializers import CopySerializer
from books.models import Book


class CopyView(ListCreateAPIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [custom_permission]

    serializer_class = CopySerializer

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs.get("pk"))

        serializer.save(book=book)

    def get_queryset(self):
        book = get_object_or_404(Book, pk=self.kwargs.get("pk"))

        return Copy.objects.filter(book=book)
