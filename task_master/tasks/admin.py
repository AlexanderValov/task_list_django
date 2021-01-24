from django.contrib import admin

from .models import Profile, Task, Subtask, Category


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'category', 'completed']


@admin.register(Subtask)
class SubtaskAdmin(admin.ModelAdmin):
    list_display = ['task', 'subtask']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
