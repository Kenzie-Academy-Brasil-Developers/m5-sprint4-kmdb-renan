from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, status
from rest_framework.response import Response
from movies.models import Movie

from movies.permissions import OnlyAdminWrite
from movies.serializers import MovieSerializer
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class MovieView(APIView, PageNumberPagination):
    permission_classes = [OnlyAdminWrite]

    def get(self, request):
        movies = Movie.objects.all()
        result_page = self.paginate_queryset(movies, request, view=self)
        instance = MovieSerializer(result_page, many=True)
        return self.get_paginated_response(instance.data)

    def post(self, request):
        movie = MovieSerializer(data=request.data)
        movie.is_valid(raise_exception=True)
        instance = movie.save()
        return Response(instance, status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    permission_classes = [OnlyAdminWrite]

    def get(self, request, id):
        movie = get_object_or_404(Movie, id=id)
        instance = MovieSerializer(movie)
        return Response(instance.data)

    def delete(self, request, id):
        movie = get_object_or_404(Movie, id=id)
        movie.delete()
        return Response({}, status.HTTP_204_NO_CONTENT)

    def patch(self, request, id):
        movie = get_object_or_404(Movie, id=id)
        serializer = MovieSerializer(movie, request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
