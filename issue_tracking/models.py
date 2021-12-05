from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    def __str__(self):
        return f'{self.email}'


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=150)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Contributor(models.Model):
    CHOICES = (
        (1, 'Add_Contributor + Remove_Contributor'),
        (2, 'Add_Contributor'),
        (3, 'No special permission'),
    )
    user_id = models.IntegerField()
    project_id = models.IntegerField()
    permission = models.IntegerField(choices=CHOICES, default=3)
    role = models.CharField(max_length=150)


class Issue(models.Model):
    title = models.CharField(max_length=150)
    desc = models.CharField(max_length=150)
    tag = models.CharField(max_length=150)
    priority = models.CharField(max_length=150)
    project_id = models.IntegerField()
    status = models.CharField(max_length=150)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author_issue")
    assignee_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignee_issue")
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=150)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateField(auto_now_add=True)
