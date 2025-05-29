from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import UserRegistrationForm, UserProfileForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Убедитесь, что пароль хешируется
            user.save()
            return redirect('login')  # Перенаправление на страницу входа после регистрации
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST, request.FILES)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             send_mail(
#                 'Добро пожаловать!',
#                 'Спасибо за регистрацию на нашем сайте.',
#                 'from@example.com',
#                 [user.email],
#                 fail_silently=False,
#             )
#             return redirect('home')  # Перенаправление на главную страницу
#     else:
#         form = UserRegistrationForm()
#     return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу после входа
        else:
            return render(request, 'users/login.html', {'error': 'Неверные учетные данные'})
    return render(request, 'users/login.html')


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Перенаправление на страницу профиля
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})
