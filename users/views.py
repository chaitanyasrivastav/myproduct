from http.client import CREATED
from django.contrib.auth.models import User
from django.views.defaults import bad_request
from django.http import HttpResponse
import json

from django.shortcuts import render
from .forms import SignupForm

from myproduct.custom_exceptions import MethodNotAllowedError, AlreadyExistsError, BadRequestError

# Create your views here.

def create_user_json(request):
    headers = {"Content-Type": "application/json"}
    response_data = {}
    if request.method == "POST":
        request_data = json.loads(request.body)
        username = request_data["firstName"]
        email = request_data["email"]
        password = request_data["password"]
        user = User.objects.filter(username=username)
        if user:
            raise AlreadyExistsError(f"{username} already exists. Try a different username.")
        user = User.objects.create_user(username, email, password)
        user.save()
        response_data["message"] = f"User {username} successfully created."
        return HttpResponse(json.dumps(response_data), headers=headers, status=CREATED)
    else:
        raise MethodNotAllowedError(f"{request.method} method is not allowed for this endpoint.")

def show_signup_page(request):
    if request.method == "GET":
        form = SignupForm()
        return render(request, "users/signup.html", {"form": form})

def create_user_html(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["firstName"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.filter(username=username)
            if user:
                return bad_request(request, AlreadyExistsError(f"{username} already exists. Try a different username."))
            user = User.objects.create_user(username, email, password)
            user.save()
            return render(request, "users/user.html", {"user": user})
        else:
            return bad_request(request, BadRequestError(f"Bad Request"))
    else:
        return bad_request(request, MethodNotAllowedError(f"{request.method} method is not allowed for this endpoint."))
