from django import forms
from django.contrib.auth.models import User
from .models import Profile, Task, Subtask


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Reapeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

        def clean_password2(self):
            cd = self.clean_password2
            if cd['password'] != cd['password2']:
                raise forms.ValidationError("Passwords don't match.")
            return cd['password2']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'body','category',)


class TaskComplete(forms.Form):
    is_done = forms.BooleanField(initial=False)


class SubtaskForm(forms.ModelForm):
    class Meta:
        model = Subtask
        fields = ['subtask']
