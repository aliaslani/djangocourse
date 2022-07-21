from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User


# Create your views here.

def index(request):
    return render(request, 'account/index.html')




def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    return render(request, 'account/register.html', {'form': form})

def login(request):
    if request.mothod == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.object.filter(username=username, password=password)
        if user.exists():
            login(user)
            return render(request, 'account/index.html')
    return render(request, 'account/login.html')
