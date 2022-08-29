from http.client import CREATED
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import AlreadyExistsError, BadRequestError
from .serializers import UserSerializer, UserAPISerializer
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, filters

# Create your views here.
class UserView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = User.objects.all()
    serializer_class = UserAPISerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'email']
    search_fields = ['first_name', 'last_name']

    def post(self, request):
        request_data = JSONParser().parse(request)
        username = request_data["username"]
        user_type = request_data["user_type"]
        password = request_data["password"]
        user = User.objects.filter(username=username)
        if user:
            raise AlreadyExistsError(f"{username} already exists. Try a different username.")
        request_data["groups"] = [user_type]
        request_data["is_staff"] = True
        request_data["password"] = make_password(password)
        serializer = UserSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            user_api_serializer = UserAPISerializer(serializer.data)
            return JsonResponse(user_api_serializer.data, status=CREATED)
        else:
            raise BadRequestError(serializer.errors)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = User.objects.all()
    serializer_class = UserAPISerializer