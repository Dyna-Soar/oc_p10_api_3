from rest_framework.permissions import BasePermission

from rest_framework import permissions

from .models import User, Project, Contributor, Issue, Comment


class IsGetOrIsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        # allow all GET requests
        if request.method == 'GET':
            return True

        # Otherwise, only allow authenticated requests
        # Post Django 1.10, 'is_authenticated' is a read-only attribute
        #return request.user and request.user.is_authenticated
        return request.user.is_authenticated


class IsAuthorOrContributorOfProject(permissions.BasePermission):

    def has_permission(self, request, view):
        project_id = request.path.split('/')[3]
        project = Project.objects.get(project_id=project_id)
        contributors = Contributor.objects.filter(project_id=project_id)

        # Is Author ?
        if request.user == project.author_user_id:
            return True

        # Is Contributor
        # Elif Is contributor of project
            # Return True
        for contributor in contributors:
            if request.user.id == contributor.user_id:
                return True


class GetOrPostContributor(permissions.BasePermission):
    """
    GET: Is contributor of project
    POST: Is contributor of project with special permission (1, 2)
    """

    def has_permission(self, request, view):
        project_id = request.path.split('/')[3]
        project = Project.objects.get(project_id=project_id)
        contributors = Contributor.objects.filter(project_id=project_id)

        if request.user == project.author_user_id:
            return True

        if request.method == "GET":
            for contributor in contributors:
                if request.user.id == contributor.user_id:
                    return True

        if request.method == "POST":
            for contributor in contributors:
                if request.user.id == contributor.user_id:
                    if contributor.permission == 1 or contributor.permission == 2:
                        return True


class DeleteContributor(permissions.BasePermission):
    """Is Contributor allowed to remove another contributor from project"""

    def has_permission(self, request, view):
        project_id = request.path.split('/')[3]
        project = Project.objects.get(project_id=project_id)
        contributors = Contributor.objects.filter(project_id=project_id)

        if request.user == project.author_user_id:
            return True

        for contributor in contributors:
            if request.user.id == contributor.user_id:
                if contributor.permission == 1:
                    return True


class GetOrPutProject(permissions.BasePermission):
    """
    Is user the author of the project
    GET: Is user a contributor of the project
    """

    def has_permission(self, request, view):
        project_id = request.path.split('/')[3]
        project = Project.objects.get(project_id=project_id)
        contributors = Contributor.objects.filter(project_id=project_id)

        if request.user == project.author_user_id:
            return True

        if request.method == "GET":
            for contributor in contributors:
                if request.user.id == contributor.user_id:
                    return True


class IsAuthorOrAssigneeOfIssue(permissions.BasePermission):

    def has_permission(self, request, view):
        issue_id = request.path.split('/')[5]
        issue = Issue.objects.get(id=issue_id)

        if request.user == issue.author_user_id:
            return True

        if request.user == issue.assignee_user_id:
            return True


class IsContributorOrAuthorOfComment(permissions.BasePermission):
    """
    GET: Is contributor or author of the project
    PUT and DELETE: Is author of the comment
    """

    def has_permission(self, request, view):
        project_id = request.path.split('/')[3]
        comment_id = request.path.split('/')[7]
        project = Project.objects.get(project_id=project_id)
        contributors = Contributor.objects.filter(project_id=project_id)
        comment = Comment.objects.get(comment_id=comment_id)

        if request.method == "GET":
            if request.user == project.author_user_id:
                return True
            for contributor in contributors:
                if request.user.id == contributor.user_id:
                    return True

        if request.method == "PUT" or request.method == "DELETE":
            if request.user == comment.author_user_id:
                return True



