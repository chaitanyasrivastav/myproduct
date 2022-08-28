from http.client import CREATED
from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import AlreadyExistsError
from .serializers import UserSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["POST"])
def create_user(request):
    response_data = {}
    request_data = JSONParser().parse(request)
    username = request_data["firstName"]
    email = request_data["email"]
    password = request_data["password"]
    user = User.objects.filter(username=username)
    if user:
        raise AlreadyExistsError(f"{username} already exists. Try a different username.")
    user = User.objects.create_user(username, email, password)
    user.save()
    response_data["message"] = f"User {email} successfully created."
    serializer = UserSerializer(user)
    return JsonResponse(serializer.data, status=CREATED)
