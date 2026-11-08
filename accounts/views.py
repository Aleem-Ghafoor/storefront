from django.shortcuts import render, redirect
from .form import RegistrationForm, loginform
from django.contrib.auth import login, logout


def register_user(request):

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/registration.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = loginform(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        
    else:
        form = loginform()

    return render(request, 'accounts/login.html', {'form': form})

def logout_user(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')
