from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import DepositForm, WithdrawalForm
from django.db.models import Sum
from .forms import UserProfileForm, TransactionForm, AccountDetailsForm


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

        return render(request, "login.html", user_info)
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


@login_required(login_url='login')
def transfer(request):
    if request.method == 'POST':
        form1 = TransactionForm(request.POST)
        if form1.is_valid():
            form1.save()
            messages.add_message(request, messages.INFO, 'Payment Successfully Done !!!')
            return redirect('home')
    else:
        form1 = TransactionForm()
    return render(request, 'transfer.html', {'form1': form1})




@login_required(login_url='login')
def update_profile_save(request, pk):
    profile = User_Profile.objects.get(id=pk)
    form = UserProfileForm(instance=profile)
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Account Updated Successfully!!!!')
            return redirect('home')

    context ={'form': form}
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def account_details(request):
    if request.method == 'POST':
        form2 = AccountDetailsForm(request.POST)
        if form2.is_valid():
            form2.save()
            messages.add_message(request, messages.INFO, 'Account Reviewed')
            return redirect('home')
    else:
        form2 = AccountDetailsForm()
    return render(request, 'profile.html', {'form': form2})


@login_required(login_url='login')
def deposit_view(request):
    form = DepositForm(request.POST or None)

    if form.is_valid():
        deposit = form.save(commit=False)
        deposit.user = request.user
        deposit.save()
        # adds users deposit to balance.
        deposit.user.account.balance += deposit.amount
        deposit.user.account.save()
        messages.success(request, 'You Have Deposited {} $.'
                         .format(deposit.amount))
        return redirect("home")

    context = {
        "title": "Deposit",
        "form": form
    }
    return render(request, "transactions/form.html", context)


@login_required(login_url='login')
def withdrawal_view(request):
    form = WithdrawalForm(request.POST or None, user=request.user)

    if form.is_valid():
        withdrawal = form.save(commit=False)
        withdrawal.user = request.user
        withdrawal.save()
        # subtracts users withdrawal from balance.
        withdrawal.user.account.balance -= withdrawal.amount
        withdrawal.user.account.save()

        messages.success(
            request, 'You Have Withdrawn {} $.'.format(withdrawal.amount)
        )
        return redirect("home")

    context = {
        "title": "Withdraw",
        "form": form
    }
    return render(request, "transactions/form.html", context)

def home2(request):
    if not request.user.is_authenticated:
        return render(request, "core/home.html", {})
    else:
        user = request.user
        deposit = Deposit.objects.filter(user=user)
        deposit_sum = deposit.aggregate(Sum('amount'))['amount__sum']
        withdrawal = Withdrawal.objects.filter(user=user)
        withdrawal_sum = withdrawal.aggregate(Sum('amount'))['amount__sum']

        context = {
                    "user": user,
                    "deposit": deposit,
                    "deposit_sum": deposit_sum,
                    "withdrawal": withdrawal,
                    "withdrawal_sum": withdrawal_sum,
                  }

        return render(request, "core/transactions.html", context)


def about(request):
    return render(request, "core/about.html", {})
