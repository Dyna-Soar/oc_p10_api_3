from django.shortcuts import render
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .models import User, Project, Contributor, Issue, Comment
from .serializers import UserSerializer, ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer

# Custom permissions
from .permissions import (IsGetOrIsAuthenticated,
                          IsAuthorOrContributorOfProject,
                          GetOrPostContributor,
                          DeleteContributor,
                          GetOrPutProject,
                          IsAuthorOrAssigneeOfIssue,
                          IsContributorOrAuthorOfComment)

# Create your views here.


class RegisterAPIView(APIView):
    """Register new user"""
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        user_data = request.data

        new_user = User.objects.create(
            username=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
        )

        # Hashing password
        new_user.set_password(new_user.password)

        new_user.save()

        serializer = UserSerializer(new_user)

        return Response(serializer.data)


class UserAPIView(APIView):
    """Show list of users or register user"""
    # Serializer class to display fields in browsable API
    serializer_class = UserSerializer
    permission_classes = [IsGetOrIsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Get user by id
        try:
            id = request.query_params["id"]
            if id != None:
                user = User.objects.get(user_id=id)
                serializer = UserSerializer(user)

        # Get all users
        except:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        user_data = request.data

        new_user = User.objects.create(
            #user_id=user_data["user_id"],
            username=user_data["email"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
        )

        # Hashing password
        new_user.set_password(new_user.password)

        new_user.save()

        serializer = UserSerializer(new_user)

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        pass


class ProjectAPIView(APIView):
    """Show projects associated with the user or create new project"""

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve projects associated with the user (author and contributor)
        projects = []

        # Projects in which the user is a contributor
        for contributor in Contributor.objects.filter(user_id=request.user.id):
            project_contributor = Project.objects.get(project_id=contributor.project_id)
            projects.append(project_contributor)

        # Projects in which the user is the author
        projects_author = Project.objects.filter(author_user_id=request.user)
        for project_author in projects_author:
            projects.append(project_author)

        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        project_data = request.data

        new_project = Project.objects.create(
            title=project_data["title"],
            description=project_data["description"],
            type=project_data["type"],
            author_user_id=request.user,
        )

        new_project.save()

        serializer = ProjectSerializer(new_project)

        return Response(serializer.data)


class ProjectIdAPIView(APIView):
    """
    GET: get a project's details by its id
    PUT: update a project
    DELETE: delete a project and its related issues
    """

    serializer_class = ProjectSerializer
    permission_classes = [GetOrPutProject]

    # Get a project's details by its id
    def get(self, request, project_id, *args, **kwargs):
        project = Project.objects.get(project_id=project_id)
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    # Update a project
    def put(self, request, project_id, *args, **kwargs):
        project_data = request.data
        project = Project.objects.get(project_id=project_id)
        if project_data["title"] != "":
            project.title = project_data["title"]
        if project_data["description"] != "":
            project.description = project_data["description"]
        if project_data["type"] != "":
            project.type = project_data["type"]
        project.save()
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    # Delete a project and its related issues
    def delete(self, request, project_id, *args, **kwargs):
        # Delete the project
        project = Project.objects.get(project_id=project_id)
        project.delete()

        # Delete related issues
        issues = Issue.objects.filter(project_id=project_id)
        for issue in issues:
            issue.delete()

        return Response(f'The project and related issues were deleted')



class ContributorsToProject(APIView):
    """
    GET: get all contributors of a project
    POST: add a user as contributor of a project
    """

    permission_classes = [GetOrPostContributor]

    # Get all contributors of a project
    def get(self, request, project_id, *args, **kwargs):
        contributors = Contributor.objects.filter(project_id=project_id)
        serializer = ContributorSerializer(contributors, many=True)
        return Response(serializer.data)

    # Add a contributor to a project
    def post(self, request, project_id, *args, **kwargs):
        contributor_data = request.data
        new_contributor = Contributor.objects.create(
            user_id=contributor_data["user_id"],
            project_id=project_id,
            permission=contributor_data["permission"],
            role=contributor_data["role"]
        )
        new_contributor.save()
        serializer = ContributorSerializer(new_contributor)
        return Response(serializer.data)


class DeleteContributorFromProject(APIView):
    """Delete contributor from project"""

    permission_classes = [DeleteContributor]

    def delete(self, request, project_id, contributor_id, *args, **kwargs):
        contributor = Contributor.objects.get(project_id=project_id, user_id=contributor_id)
        contributor.delete()
        return Response(f"contributor of id {contributor.user_id} from project {contributor.project_id} was deleted")


class ProjectIssues(APIView):
    """
    Get all issues related to a project
    Post a issue of a project
    """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthorOrContributorOfProject]

    def get(self, request, project_id, *args, **kwargs):
        # Get all isssues related to a problem
        issues = Issue.objects.filter(project_id=project_id)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, project_id, *args, **kwargs):
        # Create an Issue inside a project
        issue_data = request.data
        issue = Issue.objects.create(
            title=issue_data["title"],
            desc=issue_data["desc"],
            tag=issue_data["tag"],
            priority=issue_data["priority"],
            project_id=project_id,
            status=issue_data["status"],
            author_user_id=request.user,
            assignee_user_id=request.user
        )
        issue.save()
        serializer = IssueSerializer(issue)
        return Response(serializer.data)


class PutOrDeleteIssue(APIView):
    """
    PUT: update an issue
    DELETE: delete an issue
    """

    serializer_class = IssueSerializer
    permission_classes = [IsAuthorOrAssigneeOfIssue]

    # Update an issue
    def put(self, request, project_id, issue_id, *args, **kwargs):
        issue_data = request.data
        issue = Issue.objects.get(id=issue_id)
        if issue_data["title"] != "":
            issue.title = issue_data["title"]
        if issue_data["desc"] != "":
            issue.desc = issue_data["desc"]
        if issue_data["tag"] != "":
            issue.tag = issue_data["tag"]
        if issue_data["priority"] != "":
            issue.priority = issue_data["priority"]
        if issue_data["status"] != "":
            issue.status = issue_data["status"]
        issue.save()
        serializer = IssueSerializer(issue)
        return Response(serializer.data)

    # Delete an issue
    def delete(self, request, project_id, issue_id, *args, **kwargs):
        issue = Issue.objects.get(id=issue_id)
        issue.delete()
        return Response(f'issue from project {issue.project_id} was deleted')


class GetOrPostComment(APIView):
    """
    GET: get all comments of an issue
    POST: post a comment in an issue
    """

    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrContributorOfProject]

    # Get all comments of an issue
    def get(self, request, project_id, issue_id, *args, **kwargs):
        comments = Comment.objects.filter(issue_id=issue_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    # Post a comment for an issue
    def post(self, request, project_id, issue_id, *args, **kwargs):
        comment_data = request.data
        issue = Issue.objects.get(id=issue_id)
        comment = Comment.objects.create(
            description=comment_data["description"],
            author_user_id=request.user,
            issue_id=issue
        )
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)


class CommentIdAPIView(APIView):
    """
    GET: get details of a comment
    PUT: update a comment
    DELETE: delete a comment
    """

    serializer_class = CommentSerializer
    permission_classes = [IsContributorOrAuthorOfComment]

    # Get a comment by its id
    def get(self, request, project_id, issue_id, comment_id, *args, **kwargs):
        comment = Comment.objects.get(comment_id=comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    # Update a comment
    def put(self, request, project_id, issue_id, comment_id, *args, **kwargs):
        comment_data = request.data
        comment = Comment.objects.get(comment_id=comment_id)
        if comment_data["description"] != "":
            comment.description = comment_data["description"]
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    # Delete a comment
    def delete(self, request, project_id, issue_id, comment_id, *args, **kwargs):
        comment = Comment.objects.get(comment_id=comment_id)
        comment.delete()
        return Response(f'comment from issue {issue_id} of project {project_id} was deleted')
