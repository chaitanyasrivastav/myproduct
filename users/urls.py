from django.urls import path
from . import views

urlpatterns = [
    path('', views.CreateUserView.as_view(), name='create_user'),
    path('<str:username>', views.UserDetailView.as_view(), name='user_detail'),
]