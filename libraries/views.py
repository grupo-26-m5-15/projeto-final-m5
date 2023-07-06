from rest_framework.views import APIView, Request, Response, status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Library, LibraryBooks, LibraryEmployee, UserLibraryBlock
from .serializers import LibrarySerializer
from .permissions import IsLibraryEmployee
from users.permissions import IsAdminOrEmployee

from .models import Library, LibraryBooks, LibraryEmployee, UserLibraryBlock
from .serializers import LibrarySerializer


class ListLibraryView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrEmployee]

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer


class CreateLibraryView(CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer


class LibraryDetailViews(RetrieveUpdateDestroyAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsLibraryEmployee]

    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
