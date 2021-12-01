from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from .models import User, Project, Contributor, Issue, Comment
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer

# Create your views here.


class UserAPIView(APIView):
    # Serializer class to display fields in browsable API
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        user_data = request.data

        new_user = User.objects.create(
            #user_id=user_data["user_id"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
        )

        new_user.save()

        serializer = UserSerializer(new_user)

        return Response(serializer.data)


class ProjectAPIView(APIView):
    pass


class ContributorAPIView(APIView):
    pass


class IssueAPIView(APIView):
    pass


class CommentAPIView(APIView):
    pass
