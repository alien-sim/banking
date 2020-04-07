from django.shortcuts import render, redirect
# from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from django.conf import settings
import hashlib, datetime, random

from .forms import UserProfileForm, TransactionForm
from .models import UserActivation

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
		email_subject = 'Account confirmation'
		email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
		48hours http://127.0.0.1:8000/confirm/%s" % (username, activation_key)

		send_mail(email_subject, email_body, 'Banking App',[email], fail_silently=False)
	except Exception as e:
		print("activation lick error == ", e)

def signup_confirm(request, activation_key):
	try:
		print("signing confirm")
		user_active = UserActivation.objects.get(activation_key=activation_key)
		if user_active.key_expires < timezone.now():
			return render('confirm_expired.html')
		user_profile.is_active = True
		user_profile.save()
		return redirect('profile-form')
	except Exception as e:
		print("activation confirm error -- ", e)

def login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user:
			act_obj = UserActivation.objects.get(user=username)

			if act_obj.is_active:
				auth_login(request, user)
				return redirect('profile-form')
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

