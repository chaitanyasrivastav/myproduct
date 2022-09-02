from http.client import CREATED, OK
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import BadRequestError
from questions.models import Question, Choice
from .models import Assessment, AssessmentQuestionJunction, AssessmentUserJunction
from .serializers import AssessmentSerializer, AssessmentQuestionJunctionSerializer, AssessmentUserJunctionSerializer, StartAssessmentSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from django.db.transaction import atomic

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

    @atomic
    def post(self, request, pk):
        print("session: ", request.session.session_key)
        request_data = JSONParser().parse(request)
        questions = request_data["questions"]
        assess_ques_objs = []
        for question in questions:
            try:
                Question.objects.get(id=question, author=request.user.pk)
            except Exception:
                raise BadRequestError(f"Question [{question}] is not allowed to add as you dont own it.")
            assess_ques_obj = {
                "assessment": pk,
                "question": question
            }
            assess_ques_objs.append(assess_ques_obj)
        for assess_ques_obj in assess_ques_objs:
            serializer = AssessmentQuestionJunctionSerializer(data=assess_ques_obj)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=CREATED)
            else:
                raise BadRequestError(serializer.errors)

class AssessmentUserCreateView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = AssessmentUserJunction.objects.all()
    serializer_class = AssessmentUserJunctionSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['assessment', 'question']

    # def list(self, request, pk):
    #     request.session.delete()
    #     return JsonResponse({"a": 1})

    def post(self, request, pk):
        if request.session.session_key is not None:
            raise BadRequestError(f"Session [{request.session.session_key}] is use for this user.")
        request.session.create()
        session_id = request.session.session_key
        request.session["assessment_id"] = pk
        request.session["user"] = request.user.pk
        request.session["question_index"] = 0
        request.session["correct"] = 0
        request_data = {
            "user": request.user.pk,
            "assessment": pk,
            "session_id": session_id,
            "score": 0
        }
        serializer = AssessmentUserJunctionSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=CREATED)
        else:
            raise BadRequestError(serializer.errors)

class StartAssessmentView(APIView):
    
    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Question.objects.all()
    serializer_class = StartAssessmentSerializer

    def post(self, request, pk):
        if request.session.session_key is None:
            raise BadRequestError(f"Assessment Completed. Start a new session to retake.")
        request_data = JSONParser().parse(request)
        answers = request_data.get("answers")
        question_idx = request.session["question_index"]
        filtered_queryset = AssessmentQuestionJunction.objects.filter(assessment=pk)
        if len(filtered_queryset) <= question_idx:
            print(f"{request.session['correct']} correct out of {len(filtered_queryset)}")
            response = {
                "correct": request.session['correct'],
                "total": len(filtered_queryset)
            }
            request.session.flush()
            return JsonResponse(response)
        question_in_assessment = filtered_queryset[question_idx]
        if question_idx > 0:
            if answers:
                correct_answers = [c.id for c in Choice.objects.filter(question=question_in_assessment.question.pk, mark_as_answer=True)]
                incorrect = False
                for answer in answers:
                    if answer not in correct_answers:
                        incorrect = True
                        break
                if not incorrect:
                    request.session["correct"] += 1
            else:
                raise BadRequestError(f"No reponse recorded.")
        s = self.serializer_class(question_in_assessment.question)
        request.session["question_index"] += 1
        return JsonResponse(s.data)