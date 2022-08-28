from http.client import CREATED, NO_CONTENT, OK
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import AlreadyExistsError, NotFoundError, InternalServerError
from .serializers import UserSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["POST"])
def create_user(request):
    request_data = JSONParser().parse(request)
    username = request_data["username"]
    user = User.objects.filter(username=username)
    if user:
        raise AlreadyExistsError(f"{username} already exists. Try a different username.")
    serializer = UserSerializer(data=request_data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=CREATED)
    else:
        raise InternalServerError(serializer.errors)

@api_view(["GET", "PUT", "DELETE"])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
        serializer = UserSerializer(user)
        if request.method == "GET":
            return JsonResponse(serializer.data, status=OK)
        if request.method == "DELETE":
            user.delete()
            return HttpResponse(status=NO_CONTENT)
        if request.method == "PUT":
            request_data = JSONParser().parse(request)
            serializer = UserSerializer(user, data=request_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=OK)
            else:
                raise InternalServerError(serializer.errors)
    except User.DoesNotExist:
        raise NotFoundError(f"User with id=[{pk}] not found.")
