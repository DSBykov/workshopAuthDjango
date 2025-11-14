from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login


def home_view(request):
    return render(request, template_name='home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    elif request.method == 'GET':
        form = AuthenticationForm()
    return render(request, template_name='login.html', context={'form': form})

def signin_view(request):
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    elif request.method == 'GET':
        form = UserCreationForm()
    return render(request, template_name='signin.html', context={'form': form})

def logout_confirm(request):
    return render(request, template_name='logout.html')