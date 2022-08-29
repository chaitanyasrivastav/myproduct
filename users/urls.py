from django.urls import path
from .views import CreateUserView, UserDetailView, UserListView

urlpatterns = [
    path('', CreateUserView.as_view(), name='create_user'),
    path('list', UserListView.as_view(), name='list_user'),
    path('<str:username>', UserDetailView.as_view(), name='user_detail'),
]