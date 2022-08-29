from http.client import CREATED, NO_CONTENT, OK
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import AlreadyExistsError, NotFoundError, BadRequestError
from myproduct.questions.models import Question
from .serializers import QuestionSerializer
from rest_framework.decorators import api_view

# Create your views here.
@api_view(["POST"])
def create_question(request):
    request_data = JSONParser().parse(request)
    title = request_data["title"]
    question = Question.objects.filter(title=title)
    if question:
        raise AlreadyExistsError(f"{title} already exists. Try a different title.")
    serializer = QuestionSerializer(data=request_data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=CREATED)
    else:
        raise BadRequestError(serializer.errors)

@api_view(["GET", "PUT", "DELETE"])
def question_detail(request, title):
    try:
        question = Question.objects.get(title=title)
        serializer = QuestionSerializer(question)
        if request.method == "GET":
            return JsonResponse(serializer.data, status=OK)
        if request.method == "DELETE":
            question.delete()
            return HttpResponse(status=NO_CONTENT)
        if request.method == "PUT":
            request_data = JSONParser().parse(request)
            serializer = QuestionSerializer(question, data=request_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=OK)
            else:
                raise BadRequestError(serializer.errors)
    except question.DoesNotExist:
        raise NotFoundError(f"Question with title=[{title}] not found.")
