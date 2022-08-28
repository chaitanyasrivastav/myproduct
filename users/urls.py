from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_user_json, name='create_user_json'),
    path('signup', views.show_signup_page, name='show_signup_page'),
    path('create', views.create_user_html, name='create_user_html'),
]