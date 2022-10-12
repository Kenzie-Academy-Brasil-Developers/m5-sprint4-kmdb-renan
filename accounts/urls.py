from django.urls import path
from . import views

urlpatterns = [
    path("users/register/", views.UserView.as_view()),
    path("users/login/", views.LoginView.as_view()),
    path("users/", views.ListUsersView.as_view()),
    path("users/<int:id>/", views.UserDetailView.as_view()),
]
