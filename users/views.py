# from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from .serializers import UserSerializer

from .models import User


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
