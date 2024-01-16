from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from django.contrib import messages
from .forms import *

class RegisterView( View):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})

class LoginView( View):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': LoginForm()
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('shortner:home')
        messages.error(request, 'Invalid login credentials')
        return render(request, self.template_name)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')
