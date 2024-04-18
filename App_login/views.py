from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from App_login.serializers import LoginSerializer
from .models import Task
from .froms import TaskForm, SignUpForm
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid Username or Password')
    else:
        form = AuthenticationForm()

    context = {
        'title': 'Login',
        'form': form,
    }
    return render(request, 'App_login/login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    context = {
            'title': 'Login',
            'form': form,
        }
    return render(request, 'App_login/signup.html', context)


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user
        tasks = Task.objects.filter(user=user)

        if request.method == 'POST':
            form = TaskForm(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = user
                task.save()
                messages.success(request, 'Task added successfully.')
                return redirect('home')
        else:
            form = TaskForm()

        context = {
            'title': 'Home',
            'user': user,
            'tasks': tasks,
            'form': form,
        }
        return render(request, 'App_login/home.html', context)
    else:
        return redirect('login')


class LoginAPIView(APIView):
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)