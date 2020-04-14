from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('profile-form', views.profile_form, name='profile-form'),
    path('profile_save', views.profile_save, name='profile_save'),
    path('transfer', views.transfer, name='transfer'),
    path(r'activate_user', views.activation_page, name='activate-page'),
    url(r'^confirm/(?P<activation_key>\w+)/$', views.signup_confirm,name='signup-confirm'),
    path('create-account', views.create_account, name='create-account'),
    path('transactions', views.transaction, name='transaction'),
    path('add-transaction', views.add_transaction, name='add-transaction'),
    path('accountbalance', views.account_balance, name='account-balance'),
    # path('tryemail', views.try_email, name='try-email'),
    path('logout', views.logout, name='logout'),
]