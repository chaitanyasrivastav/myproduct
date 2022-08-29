from http.client import CREATED, NO_CONTENT, OK
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import AlreadyExistsError, NotFoundError, BadRequestError
from .serializers import UserSerializer, UserAPISerializer
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework import filters

# Create your views here.
class UserListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserAPISerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'email']
    search_fields = ['first_name', 'last_name']

class CreateUserView(APIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = User.objects.all()

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

class UserDetailView(APIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = User.objects.all()

    def get_object(self, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFoundError(f"User with username=[{username}] not found.")

    def get(self, request, username):
        user = self.get_object(username)
        serializer = UserAPISerializer(user)
        return JsonResponse(serializer.data, status=OK)

    def put(self, request, username):
        user = self.get_object(username)
        request_data = JSONParser().parse(request)
        serializer = UserAPISerializer(user, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=OK)
        else:
            raise BadRequestError(serializer.errors)

    def delete(self, request, username):
        user = self.get_object(username)
        user.delete()
        return HttpResponse(status=NO_CONTENT)