from django.db import models

# Create your models here.


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    type = models.CharField(max_length=150)
    author_user_id = models.ForeignKey(User, on_delete=models.CASCADE)


class Contributor(models.Model):
    user_id = models.ManyToManyField(User)
    project_id = models.IntegerField()
    role = models.CharField(max_length=150)


class Issue(models.Model):
    title = models.CharField(max_length=150)
    desc = models.CharField(max_length=150)
    tag = models.CharField(max_length=150)
    priority = models.CharField(max_length=150)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
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
