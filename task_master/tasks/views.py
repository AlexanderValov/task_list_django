from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import LoginForm, UserRegistrationForm, TaskForm, TaskComplete, SubtaskForm
from .models import Profile, Task, Category


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'tasks/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'tasks/register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disable account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'tasks/login.html', {'form': form})


@login_required
def dashboard(request):
    tasks = Task.objects.filter(completed=False)
    categories = Category.objects.all()
    context = {
        'tasks': tasks,
        'categories': categories
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def get_category(request, pk):
    tasks = Task.objects.filter(category=pk)
    categories = Category.objects.all()
    context = {
        'tasks': tasks,
        'categories': categories
    }
    return render(request, 'tasks/dashboard.html', context)


@login_required
def completed_task(request):
    tasks = Task.objects.filter(completed=True)
    categories = Category.objects.all()
    context = {
        'tasks': tasks,
        'categories': categories
    }
    return render(request, 'tasks/completed_tasks.html', context)


@login_required
def task_detail(request, pk):
    task = get_object_or_404(Task, id=pk)
    subtasks = task.subtask.all()
    new_subtask = None
    if request.method == 'POST' and 'subtask' in request.POST:
        subtask_form = SubtaskForm(request.POST)
        if subtask_form.is_valid():
            new_subtask = subtask_form.save(commit=False)
            new_subtask.task = task
            new_subtask.save()
            return redirect(task)
    else:
        subtask_form = SubtaskForm()

    if request.method == 'POST' and 'is_done' in request.POST:
        form_complete = TaskComplete(request.POST)
        if form_complete.is_valid():
            task.completed = form_complete.cleaned_data['is_done']
            task.save()
            return redirect(completed_task)
    else:
        form_complete = TaskComplete()

    context = {
        'task': task,
        'form_complete': form_complete,
        'subtask_form': subtask_form,
        'subtasks': subtasks,
        'new_subtask': new_subtask
    }
    return render(request, 'tasks/task_detail.html', context)


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.delete()
    return redirect('dashboard')


@login_required
def add_task(request):
    new_task = None
    if request.method == 'POST':
        task_form = TaskForm(data=request.POST)
        if task_form.is_valid():
            new_task = task_form.save(commit=False)
            new_task.created = timezone.now()
            new_task.save()
            return redirect(new_task)
    else:
        task_form = TaskForm()
    context = {
        'task_form': task_form,
        'new_task': new_task
    }
    return render(request, 'tasks/new_task.html', context)
