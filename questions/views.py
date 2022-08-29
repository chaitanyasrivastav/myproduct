from http.client import CREATED, NO_CONTENT, OK
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import AlreadyExistsError, NotFoundError, BadRequestError
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

# Create your views here.
class CreateQuestionView(APIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Question.objects.all()

    def post(self, request):
        request_data = JSONParser().parse(request)
        title = request_data["title"]
        request_data["author"] = request.user.pk
        question = Question.objects.filter(title=title)
        if question:
            raise AlreadyExistsError(f"{title} already exists. Try a different title.")
        serializer = QuestionSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=CREATED)
        else:
            raise BadRequestError(serializer.errors)

class QuestionDetailView(APIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Question.objects.all()

    def get_object(self, title):
        try:
            return Question.objects.get(title=title)
        except Question.DoesNotExist:
            raise NotFoundError(f"Question with title=[{title}] not found.")

    def get(self, request, title):
        question = self.get_object(title)
        serializer = QuestionSerializer(question)
        return JsonResponse(serializer.data, status=OK)

    def put(self, request, title):
        question = self.get_object(title)
        request_data = JSONParser().parse(request)
        request_data["author"] = request.user.pk
        serializer = QuestionSerializer(question, data=request_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=OK)
        else:
            raise BadRequestError(serializer.errors)

    def delete(self, request, title):
        question = self.get_object(title)
        question.delete()
        return HttpResponse(status=NO_CONTENT)