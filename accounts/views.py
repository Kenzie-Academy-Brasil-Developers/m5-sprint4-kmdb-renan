from django.shortcuts import get_object_or_404
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from accounts import serializers
from accounts.models import User
from accounts.permissions import OnlyAdminSee, OnlyAdminOrItself
from accounts.serializers import LoginSerializer, RegisterUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination


# Create your views here.


class UserView(APIView):

    def post(self, request):
        animal = RegisterUserSerializer(data=request.data)
        animal.is_valid(raise_exception=True)

        instance = animal.save()

        return Response(instance, status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            token, created = Token.objects.get_or_create(user=user)

            return Response({"token": token.key})

        return Response({"detail": "invalid username or password"}, status.HTTP_400_BAD_REQUEST)


class ListUsersView(APIView, PageNumberPagination):
    permission_classes = [OnlyAdminSee]

    def get(self, request):
        users = User.objects.all()
        result_page = self.paginate_queryset(users, request, view=self)
        instance = RegisterUserSerializer(result_page, many=True)
        return self.get_paginated_response(instance.data)


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated, OnlyAdminOrItself]

    def get(self, request, id):
        user = get_object_or_404(User, id=id)

        self.check_object_permissions(request, user)

        serializer = RegisterUserSerializer(user)
        return Response(serializer.data)
