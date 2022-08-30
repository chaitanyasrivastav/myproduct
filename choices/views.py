from http.client import OK
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from myproduct.custom_exceptions import BadRequestError
from .models import Choice
from .serializers import ChoiceSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import generics

# Create your views here.
class CreateChoiceView(generics.ListCreateAPIView):

    permission_classes = [IsAuthenticated & DjangoModelPermissions]
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        else:
            author_id = self.request.query_params.get("author", None)
            if not author_id:
                author_id = self.request.user.pk
            if int(author_id) == self.request.user.pk:
                return Choice.objects.filter(author=user.pk)
            else:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return super().get_queryset()
        else:
            author_id = self.request.query_params.get("author", None)
            if not author_id:
                author_id = self.request.user.pk
            if int(author_id) == self.request.user.pk:
                return Choice.objects.filter(author=user.pk)
            else:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")

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
                return Choice.objects.get(pk=self.kwargs[self.lookup_field] ,author=user.pk)
            except Exception:
                raise BadRequestError(f"You dont have permission to view this resource as you dont own it.")

    def put(self, request, pk):
        request_data = JSONParser().parse(request)
        choice = self.get_object()
        serializer = ChoiceSerializer(choice, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=OK)
        else:
            raise BadRequestError(serializer.errors)