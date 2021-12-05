from django.urls import path, include

from .views import (RegisterAPIView,
                    UserAPIView,
                    ProjectAPIView,
                    ProjectIdAPIView,
                    ContributorsToProject,
                    DeleteContributorFromProject,
                    ProjectIssues,
                    PutOrDeleteIssue,
                    GetOrPostComment,
                    CommentIdAPIView)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('user/', UserAPIView.as_view()),
    path('project/', ProjectAPIView.as_view()),
    path('project/<int:project_id>/', ProjectIdAPIView.as_view()),
    path('project/<int:project_id>/users/', ContributorsToProject.as_view()),
    path('project/<int:project_id>/users/<int:contributor_id>/', DeleteContributorFromProject.as_view()),
    path('project/<int:project_id>/issues/', ProjectIssues.as_view()),
    path('project/<int:project_id>/issues/<int:issue_id>/', PutOrDeleteIssue.as_view()),
    path('project/<int:project_id>/issues/<int:issue_id>/comments/', GetOrPostComment.as_view()),
    path('project/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/', CommentIdAPIView.as_view()),
]