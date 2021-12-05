from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Project, Contributor, Issue, Comment

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
