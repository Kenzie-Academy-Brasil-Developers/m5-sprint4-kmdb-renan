from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, status
from rest_framework.response import Response
from movies.models import Movie
from reviews import serializers
from reviews.models import Review
from reviews.permissions import AdminOrCritic
from reviews.serializers import ReviewListSerializer, ReviewSerializer
from rest_framework.pagination import PageNumberPagination


# Create your views here.


class ReviewView(APIView, PageNumberPagination):
    permission_classes = [AdminOrCritic]

    def post(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        request.data["movie_id"] = movie.id
        request.data["critic"] = request.user.id
        serializer = ReviewSerializer(
            data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(instance, status.HTTP_201_CREATED)

    def get(self, request, movie_id):
        reviews = Review.objects.filter(movie_id=movie_id)
        results_page = self.paginate_queryset(reviews, request, view=self)
        serializer = ReviewListSerializer(results_page, many=True)
        return self.get_paginated_response(serializer.data)


class ReviewDetailView(APIView, PageNumberPagination):
    permission_classes = [AdminOrCritic]

    def get(self, request, movie_id, review_id):
        review = get_object_or_404(Review, id=review_id, movie_id=movie_id)
        serializer = ReviewListSerializer(review)
        return Response(serializer.data)

    def delete(self, request, movie_id, review_id):
        review = get_object_or_404(Review, id=review_id, movie_id=movie_id)
        self.check_object_permissions(request, review.critic)
        review.delete()
        return Response({}, status.HTTP_204_NO_CONTENT)
