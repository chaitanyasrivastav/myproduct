from http.client import CREATED, NO_CONTENT, OK
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import AlreadyExistsError, NotFoundError, InternalServerError, BadRequestError
from .serializers import QuestionSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["POST"])
def create_question(request):
    request_data = JSONParser().parse(request)
    username = request_data["username"]
    user = User.objects.filter(username=username)
    if user:
        raise AlreadyExistsError(f"{username} already exists. Try a different username.")
    serializer = QuestionSerializer(data=request_data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=CREATED)
    else:
        raise InternalServerError(serializer.errors)

@api_view(["GET", "PUT", "DELETE"])
def question_detail(request, username):
    try:
        user = User.objects.get(username=username)
        serializer = QuestionSerializer(user)
        if request.method == "GET":
            return JsonResponse(serializer.data, status=OK)
        if request.method == "DELETE":
            user.delete()
            return HttpResponse(status=NO_CONTENT)
        if request.method == "PUT":
            request_data = JSONParser().parse(request)
            serializer = QuestionSerializer(user, data=request_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=OK)
            else:
                raise BadRequestError(serializer.errors)
    except User.DoesNotExist:
        raise NotFoundError(f"User with username=[{username}] not found.")
