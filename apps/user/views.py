from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth import authenticate, get_user_model
from django.urls import reverse
from .models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.backends import ModelBackend

User = get_user_model()
# Create your views here.
def main(request):
    return render(request, 'user/main.html')

def login(request):
    if request.method == 'POST':
        id = request.POST['id']  
        password = request.POST['password']

        user = auth.authenticate(request, username=id, password=password)

        if user is None:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
            return redirect(reverse('user:login'))
            
        else:
            print('login')
            auth.login(request, user)
            if not user.height or not user.weight or not user.age or not user.gender:
                return redirect('user:additional')
            return redirect('user:main')
        
    return render(request, 'user/login.html') 

def logout(request) :
    auth.logout(request)
    return redirect(reverse('user:main'))

def signup(request):   
    if request.method == 'POST':
        first_name = request.POST['first_name'] 
        id = request.POST['id']
        email = request.POST['email']
        password = request.POST['password']
        
        hashed_password = make_password(password)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': first_name,
                'username': id,
                'password': hashed_password,
            }
        )

        if not created:
            messages.error(request, '이미 존재하는 아이디입니다.')
            return redirect(reverse('user:signup'))

        if created:
            user.backend = f'{ModelBackend.__module__}.{ModelBackend.__qualname__}'
            user.save()
            return redirect('user:main')
        else:
            return render(request, 'user/signup.html', {'error_message': '이미 해당 아이디로 가입된 유저가 있습니다.'})

    return render(request, 'user/signup.html')

def additional(request):
    if request.method == 'POST':
        user = request.user
        user.height = request.POST['height']
        user.weight = request.POST['weight']
        user.age = request.POST['age']
        user.gender = request.POST['gender']
        user.save()
        return redirect('user:additional_fitness_goal')

    return render(request, 'user/additional.html')

def additional_fitness_goal(request):
    if request.method == 'POST':
        user = request.user
        user.fitness_goal = request.POST['fitness_goal']
        user.save()
        return redirect('user:additional_activity_level')

    return render(request, 'user/additional_fitness_goal.html')

def additional_activity_level(request):
    if request.method == 'POST':
        user = request.user
        user.activity_level = request.POST['activity_level']
        user.save()
        return redirect('user:main')

    return render(request, 'user/additional_activity_level.html')

def mypage(request):
    return render(request, 'user/mypage.html')

def header(request):
    return render(request, 'user/header.html')