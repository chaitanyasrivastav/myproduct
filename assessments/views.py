from http.client import CREATED, OK
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import BadRequestError
from .models import Assessment, AssessmentQuestionJunction
from .serializers import AssessmentSerializer, AssessmentQuestionJunctionSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class CreateAssessmentView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
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
                return Assessment.objects.filter(author=user.pk)
            else:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")

    def post(self, request):
        request_data = JSONParser().parse(request)
        request_data["author"] = request.user.pk
        serializer = AssessmentSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=CREATED)
        else:
            raise BadRequestError(serializer.errors)

class AssessmentDetailView(generics.RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer

    def get_object(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_object()
        else:
            try:
                return Assessment.objects.get(pk=self.kwargs[self.lookup_field] ,author=user.pk)
            except Exception:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")

    def put(self, request, pk):
        request_data = JSONParser().parse(request)
        question = self.get_object()
        serializer = AssessmentSerializer(question, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=OK)
        else:
            raise BadRequestError(serializer.errors)

class AssessmentQuestionCreateView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = AssessmentQuestionJunction.objects.all()
    serializer_class = AssessmentQuestionJunctionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['assessment', 'question']

    def post(self, request, pk):
        request_data = JSONParser().parse(request)
        questions = request_data["questions"]
        question_objs = []
        for question in questions:
            assess_ques_obj = {
                "assessment": pk,
                "question": question
            }
            question_objs.append(assess_ques_obj)
        for question_obj in question_objs:
            serializer = AssessmentQuestionJunctionSerializer(data=question_obj)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=CREATED)
            else:
                raise BadRequestError(serializer.errors)