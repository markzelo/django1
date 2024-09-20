from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
# from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm

from .models import Task
from django.utils import timezone

from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],  # metodo post de ocultamiento importe
                                                password=request.POST['password1'])
                user.save()
                login(request, user)  # guardado de usuario
                return redirect('task')
            except IntegrityError:  # validacion de errores especificos
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'pass no coincide'
        })

@login_required
def task(request):
    # listar todas la tareas
    # tasks = Task.objects.all()
    # filtrar
    tasks = Task.objects.filter(user=request.user, datecomplete__isnull=True)
    # envio de datos al html
    return render(request, 'task.html', {'tasks': tasks})

@login_required
def task_completed(request):
    tasks = Task.objects.filter(user=request.user, datecomplete__isnull=False).order_by
    ('-datecomplete')       # consulta a bd
    # envio de datos al html
    return render(request, 'task.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm})

    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)  # condicion inicial
            new_task.user = request.user
            new_task.save()

            return redirect('task')
        except ValueError:  # devuelve  la comprobacion
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'por favor provee datos validos para la tarea'
            })

@login_required
def task_detail(request, task_id):

    if request.method == 'GET':
        # para evitar que el servidor se caiga
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
         try:
             task = get_object_or_404(Task, pk=task_id, user=request.user)   # mostrar y editar solo mis tareas
             # toma nuevos datos del formulario
             form = TaskForm(request.POST, instance=task)
             form.save()
             return redirect('task')  # envio a la pagina tareas
         except ValueError:
                return render(request, 'task_detail.html', {'task': task, 'form': form ,
                                                          'error':"error al actualizar tarea"})

@login_required       
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
       task.datecomplete = timezone.now()
       task.save()
       return redirect('task')


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
       
       task.delete()
       return redirect('task')

@login_required
def signout(request):
    logout(request)
    return redirect('home')

# comprobacion

def signin(request):
    if request.method == 'GET':  #si llega un tipo get
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:   #de lo contrario si llegan datos
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])  #verificacion de datos validos
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'usuario o password incorrecto'
            })
        else:
            login(request, user)
            return redirect('task')
