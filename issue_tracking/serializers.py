from rest_framework.serializers import ModelSerializer

from .models import User, Project, Contributor, Issue, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["user_id", "first_name", "last_name", "email", "password"]


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = []


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = []


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = []


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = []

