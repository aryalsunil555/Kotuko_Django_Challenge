
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from exam.views import AddTodoListView, BrowseMyTodoList, TodoDetail, UserLoginView, UserProfileView, UserRegistrationView
from exam import views


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('view_profile/', UserProfileView.as_view(), name='Profile'),
    path('add_todolist/', AddTodoListView.as_view(), name="addtodo"),
    path('my_todolist/', BrowseMyTodoList.as_view(), name="mytodo"),
    path('todo_detail/<int:pk>/', TodoDetail.as_view(), name="detail"),
]