# from django.shortcuts import render
from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAccountOwner, IsAdminOrEmployee
from rest_framework import permissions
from .serializers import UserSerializer
from libraries.models import LibraryEmployee
from .models import User


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrEmployee]

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [IsAdminOrEmployee]
        elif self.request.method == "POST":
            self.permission_classes = [permissions.AllowAny]
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save()

        is_admin = serializer.validated_data.get("is_admin")

        # if is_admin == True:
        #     employeeUser = LibraryEmployee.objects.create(
        #         employee=user,
        #     )


class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
