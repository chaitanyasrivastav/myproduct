from http.client import CREATED, OK
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import BadRequestError
from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import generics, filters

# Create your views here.
class CreateQuestionView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['author']
    search_fields = ['title']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        else:
            author_id = self.request.query_params.get("author", None)
            if not author_id:
                author_id = self.request.user.pk
            if int(author_id) == self.request.user.pk:
                return Question.objects.filter(author=user.pk)
            else:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")

    def post(self, request):
        request_data = JSONParser().parse(request)
        request_data["author"] = request.user.pk
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

    def get_object(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_object()
        else:
            try:
                return Question.objects.get(pk=self.kwargs[self.lookup_field] ,author=user.pk)
            except Exception:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")

    def put(self, request, pk):
        request_data = JSONParser().parse(request)
        question = self.get_object()
        serializer = QuestionSerializer(question, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=OK)
        else:
            raise BadRequestError(serializer.errors)

class CreateChoiceView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    filter_backends = [filters.SearchFilter]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        else:
            author_id = self.request.query_params.get("author", None)
            if not author_id:
                author_id = self.request.user.pk
            if int(author_id) == self.request.user.pk:
                question_id = self.kwargs["question_id"]
                return Choice.objects.filter(question=question_id, author=user.pk)
            else:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")

    def post(self, request, question_id):
        request_data = JSONParser().parse(request)
        request_data["author"] = request.user.pk
        request_data["question"] = question_id
        serializer = ChoiceSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=CREATED)
        else:
            raise BadRequestError(serializer.errors)

class ChoiceDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_object(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_object()
        else:
            try:
                question_id = self.kwargs["question_id"]
                return Choice.objects.get(pk=self.kwargs[self.lookup_field], question=question_id, author=user.pk)
            except Exception:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")

    def put(self, request, question_id, pk):
        request_data = JSONParser().parse(request)
        choice = self.get_object()
        serializer = ChoiceSerializer(choice, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=OK)
        else:
            raise BadRequestError(serializer.errors)