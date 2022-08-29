from http.client import CREATED, OK
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import AlreadyExistsError, BadRequestError
from .models import Question
from .serializers import QuestionSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class CreateQuestionView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author']
    search_fields = ['title']

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

class QuestionDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def put(self, request, pk):
        request_data = JSONParser().parse(request)
        question = self.get_object()
        serializer = QuestionSerializer(question, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=OK)
        else:
            raise BadRequestError(serializer.errors)