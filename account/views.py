from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from django.utils import timezone
from django.conf import settings
import hashlib, datetime, random

from .forms import UserProfileForm, TransactionForm
from .models import UserActivation, User_Profile

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
        send_activation_mail(request, user)
        messages.add_message(request, messages.INFO, 'Successfully User registered.')
        return redirect('login')
    else:
    	
    	return render(request, 'signup.html')

def send_activation_mail(request, user):
	try:
		username = user.username
		email = settings.ADMIN_EMAIL
		salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
		activation_key = hashlib.sha1(str(salt+email).encode('utf-8')).hexdigest()
		key_expires = datetime.datetime.today() + datetime.timedelta(2)

		# Create and save user Activation
		active_info = UserActivation(user=user, activation_key=activation_key, key_expires=key_expires)
		active_info.save()

		# Send email with activation key
		# email_subject = 'Account confirmation'
		# email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
		# 48hours http://127.0.0.1:8000/confirm/%s" % (username, activation_key)

		# send_mail(email_subject, email_body, 'Banking App',[email], fail_silently=False)
	except Exception as e:
		print("activation lick error == ", e)

def signup_confirm(request, activation_key):
	try:
		print("signing confirm")
		user_active = UserActivation.objects.get(activation_key=activation_key)
		if user_active.key_expires < timezone.now():
			return render('confirm_expired.html')
		user_active.is_active = True
		user_active.save()
		return redirect('activate-page')
	except Exception as e:
		print("activation confirm error -- ", e)

def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			if user.is_superuser:
				auth_login(request, user)
				return redirect('profile-form')
			else:
				act_obj = UserActivation.objects.get(user=user.id)
				if act_obj.is_active:
					auth_login(request, user)
					return redirect('profile-form')
				else:
					return render(request,"not_activated.html")
		else:
			messages.add_message(request, messages.INFO, 'The username and/or password you specified are not correct.')
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
		profile = User_Profile.objects.filter(user=request.user).values()
		print(profile[0])
		if profile:
			
			profileform = UserProfileForm(initial=profile[0])
			type_form = 'edit'
		else:
			profileform = UserProfileForm()
			type_form = 'create'
		form = {
        	'profileform' : profileform,
        	'type_form' : type_form

        }
		return render(request, "profile.html",form)
	except Exception as e:
		print("error in profile-form redirect")

@login_required(login_url='login')
def profile_save(request):
	try:
		type_form = 'edit'
		if type_form == 'edit':
			print(type_form)
			instance = get_object_or_404(User, id=request.user.id)
			saveProfile = UserProfileForm(request.POST, request.FILES, instance=instance)
			if saveProfile.is_valid():
				print(request.POST)

				saveProfile.save(commit=True)
			return redirect('profile-form')
		else:
			print("new profile")
			instance = User.objects.get(username= request.user)
			saveProfile = UserProfileForm(request.POST, request.FILES)
			if saveProfile.is_valid():
				saveProfile.save(commit=False)
				post.user = instance
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

def activation_page(request):
	try:
		print("@@")
		not_active = UserActivation.objects.filter(is_active=False)
		print("nott ", not_active)
		return render(request, 'activate_user.html',{'activate':not_active})
	except Exception as e:
		print("actcivation page -- ",str(e))
