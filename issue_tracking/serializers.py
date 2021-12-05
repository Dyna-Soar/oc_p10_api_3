from rest_framework.serializers import ModelSerializer

from .models import User, Project, Contributor, Issue, Comment


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "password"]


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["project_id", "title", "description", "type", "author_user_id"]


class ContributorSerializer(ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["user_id", "project_id", "permission", "role"]


class IssueSerializer(ModelSerializer):
    class Meta:
        model = Issue
        fields = ["id", "title", "desc", "tag", "priority", "project_id", "status", "author_user_id",
                  "assignee_user_id", "created_time"]


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ["comment_id", "description", "author_user_id", "issue_id", "created_time"]

