from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import UserProfileForm, TransactionForm

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
        return redirect('login')
    else:
    	
    	return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # print("mmmmm",messages.SUCCESS)
        if user:
            auth_login(request, user)
            return redirect('profile-form')
        else:
            messages.add_message(request, messages.INFO, 'The username and/or password you specified are not correct.')
            # print("mmmmm",messages.INFO)
            return redirect('login')
    else:
        return render(request, 'login.html')


@login_required(login_url='login')
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')
def profile_form(request):
	try:
		profileform = UserProfileForm()
		form = {
        	'profileform' : profileform
        }
		return render(request, "profile.html",form)
	except Exception as e:
		print("error in profile-form redirect")

@login_required(login_url='login')
def profile_save(request):
	try:
		print("save profile", request.user)
		saveProfile = UserProfileForm(request.POST,request.FILES)
		if saveProfile.is_valid():
			post = saveProfile.save(commit=False)
			post.user = User.objects.get(username= request.user)
			post.save()
			return redirect('home')
		else:
			return render(request, "profile.html", {'profileform' : saveProfile})
	except Exception as e:
		print("profile save error == ", e)

@login_required(login_url='login')
def transfer(request):
    if request.method == 'POST':
        form1 = TransactionForm(request.POST)
        if form1.is_valid():
            form1.save()
            messages.add_message(request, messages.INFO, 'Payment Successfully Done@@')
            return redirect('home')
    else:
        form1 = TransactionForm()
    return render(request, 'transfer.html', {'form1': form1})

