from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm

# Create your views here.

def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()

            return redirect('polls:index') ## to app polls with url with name index

    else:
        form = RegisterForm(response.POST)

    context = {
        "form": form
    }
    return render(response, "register/register.html", context)
