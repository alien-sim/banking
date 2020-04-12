from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

from django.utils import timezone
from django.conf import settings
import hashlib, datetime, random

from .forms import UserProfileForm, TransactionForm, AccountForm
from .models import UserActivation, User_Profile, Account_details, Transactions

@login_required(login_url='login')
def home(request):
	print ("$$$$",request)
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
				return redirect('home')
			else:
				act_obj = UserActivation.objects.get(user=user.id)
				if act_obj.is_active:
					auth_login(request, user)
					return redirect('home')
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
				post = saveProfile.save(commit=False)
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

@login_required(login_url='login')
def activation_page(request):
	try:
		not_active = UserActivation.objects.filter(is_active=False)
		print("nott ", not_active)
		return render(request, 'activate_user.html',{'activate':not_active})
	except Exception as e:
		print("actcivation page -- ",str(e))

@login_required(login_url='login')
def create_account(request):
	try:
		if request.POST:
			new_acc = AccountForm(request.POST)
			user =  User.objects.get(id= request.user.id)
			if new_acc.is_valid():
				acc = new_acc.save(commit=False)
				acc.current_user = request.user.id
				acc.user = user
				print(acc)
				new_acc.save()
				return redirect('home')
			else:
				print("not is_valid")
				return redirect('create-account')

		else:
			acc_exist = Account_details.objects.filter(current_user=request.user.id)
			if acc_exist:
				data = {
					'msg' : 'Account already exist'
				}
			else:
				data = {
					'form' : AccountForm()
				}
			return render(request, 'create_account.html',data)
	except Exception as e:
		print("crete account Exception :: ", e)

@login_required(login_url='login')
def transaction(request):
	try:
		transaction = Transactions.objects.filter(current_user=request.user.id).values().order_by('-datetime')
		return render(request, 'transaction.html',{'transaction':transaction} )
	except Exception as e:
		print("transaction error -- ", e)

@login_required(login_url='login')
def add_transaction(request):
	try:
		if request.POST:
			flag = 0
			account = Account_details.objects.get(current_user=request.user.id)
			print("1111",account)
			current_balance = float(account.balance)
			transaction_type = request.POST.get('transaction_type')
			amount = float(request.POST.get('amount'))

			recipient = Account_details.objects.get(id=request.POST.get('recipient_acc'))
			if recipient:
				print("1111", recipient.balance)
				recipient_balance = float(recipient.balance)
				if transaction_type == 'Transfer':
					if current_balance > amount:
						new_balance = current_balance - amount
						recipient_new_balance = recipient_balance + amount
						flag = 1
					else:
						messages.add_message(request, messages.INFO, 'Transaction not Possible because of insufficient balance')
						return redirect('add-transaction')
				elif transaction_type == 'Credit':
					new_balance = float(current_balance) + float(amount)
					flag = 1
			else:
				messages.add_message(request, messages.INFO, 'Recipient Account Id not correct.')
				return redirect('add-transaction')

			if flag :

				print("yesssss")
				account.balance = new_balance
				print("acco--------", account)
				account.save()
				recipient1 = Account_details.objects.get(id=request.POST.get('recipient_acc'))
				recipient1.balance = recipient_new_balance
				recipient1.save()

				new_transaction(request, new_balance)

				# new_transaction = TransactionForm(request.POST,instance=recipient)
				# if new_transaction.is_valid():
				# 	transaction = new_transaction.save(commit=False)
				# 	transaction.current_user = request.user.id
				# 	transaction.balance = new_balance
				# 	transaction.recipient_acc = recipient
				# 	# print("yess--33", transaction)
				# 	transaction.save()
					
				# else:
				# 	print(new_transaction.errors)

				return redirect('transaction')
			else:
				print("not is_valid")
				return redirect('create-account')

		else:
			form = TransactionForm()
			return render(request, "add_transaction.html", { 'form': form })
	except Exception as e:
		print("add-transaction error", e)

def new_transaction(request, new_balance):
	try:
		form_data = request.POST
		print("new_transaction")
		recipient = Account_details.objects.get(id=form_data.get('recipient_acc'))
		new_transaction = TransactionForm(form_data,instance=recipient)
		if new_transaction.is_valid():
			transaction = new_transaction.save(commit=False)
			transaction.current_user = request.user.id
			transaction.balance = new_balance
			# transaction.recipient_acc = recipient
			# print("yess--33", transaction)
			transaction.save()
			
		else:
			print(new_transaction.errors)
	except Exception as e:
		print("new transaction error",e)
