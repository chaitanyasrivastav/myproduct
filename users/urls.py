from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_user, name='create_user'),
    path('<int:pk>', views.user_detail, name='user_detail'),
]