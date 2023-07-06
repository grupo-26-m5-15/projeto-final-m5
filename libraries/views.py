from rest_framework.views import APIView, Request, Response, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Library, LibraryBooks, LibraryEmployee, UserLibraryBlock
from .serializers import LibrarySerializer


class LibraryViews(ListCreateAPIView):
    ...


class LibraryDetailViews(RetrieveUpdateDestroyAPIView):
    ...


class LibraryRetrieverBookViews(ListCreateAPIView):
    pass
