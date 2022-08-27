from http.client import CREATED
from django.contrib.auth.models import User
from django.http import HttpResponse
import json

from myproduct.custom_exceptions import MethodNotAllowedError, AlreadyExistsError

# Create your views here.

def create_user(request):
    headers = {"Content-Type": "application/json"}
    response_data = {}
    if request.method == "POST":
        request_data = json.loads(request.body)
        user = User.objects.get(username=request_data["firstName"])
        if user:
            raise AlreadyExistsError(f"{user.username} already exists. Try a different username.")
        user = User.objects.create_user(request_data["firstName"], request_data["email"], request_data["password"])
        user.last_name = request_data["lastName"]
        user.save()
        response_data["message"] = f"User {request_data['email']} successfully created."
        return HttpResponse(json.dumps(response_data), headers=headers, status=CREATED)
    else:
        raise MethodNotAllowedError(f"{request.method} method is not allowed for this endpoint.")
