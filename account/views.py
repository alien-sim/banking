from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        user.save()
        messages.add_message(request, messages.INFO, 'Successfully User registered.')
        # return redirect('login')
        user_info = {
        	'username' : user.username,
        	'email' : user.email
        }

        return render(request, "profile.html",user_info)
    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.INFO, 'The username and/or password you specified are not correct.')
            return redirect('login')
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('login')

def profile_save(request):
	try:
		print("save profile")
		return render(request, "profile.html")
	except Exception as e:
		print("profile save error == ", e)
	
