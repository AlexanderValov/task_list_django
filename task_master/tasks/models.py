from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)


class Task(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='category', null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    body = models.TextField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task_detail', args=[self.id])

    class Meta:
        ordering = ('-created',)


class Subtask(models.Model):
    task = models.ForeignKey(
        Task, on_delete=models.CASCADE, related_name='subtask')
    subtask = models.CharField(max_length=250, blank=True)
