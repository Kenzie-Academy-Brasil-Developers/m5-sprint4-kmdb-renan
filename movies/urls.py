from django.urls import path
from . import views

urlpatterns = [
    path("movies/", views.MovieView.as_view()),
    path("movies/<int:id>/", views.MovieDetailView.as_view()),
]
