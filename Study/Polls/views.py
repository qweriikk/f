from django.shortcuts import render, redirect
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .models import Article

def main(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            articles = Article.objects.order_by('-created_at')[:10]
            return render(request, "main.html", {'articles': articles})       
        else:
            return redirect("register")
def auth(request):
    if request.user.is_authenticated:
        # Если пользователь уже аутентифицирован, перенаправляем его на главную страницу или на страницу, которую он пытался посетить
        return redirect('main')  # Замените 'home' на имя вашего представления или URL

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Получаем данные из формы
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Пытаемся аутентифицировать пользователя
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Если пользователь существует и введены правильные данные, выполняем вход
                login(request, user)
                # Перенаправляем пользователя на нужную страницу
                next_url = request.GET.get('next', 'main')
                return redirect(next_url)
            else:
                # Если пользователь не найден или данные неверны, выводим сообщение об ошибке
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        # Если запрос не методом POST, просто отображаем пустую форму
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def register_view(request):
    if request.user.is_authenticated:
        # Если пользователь уже аутентифицирован, перенаправляем его на главную страницу
        return redirect('main')  # Замените 'home' на имя вашего представления или URL

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Сохраняем нового пользователя
            form.save()
            # Аутентифицируем нового пользователя и выполняем вход
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Перенаправляем пользователя на нужную страницу
                return redirect('main')  # Замените 'home' на имя вашего представления или URL
    else:
        # Если запрос не методом POST, просто отображаем пустую форму регистрации
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})