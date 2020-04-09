from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('profile_save', views.profile_save, name='profile_save'),
    path('update_profile_save/<str:pk>', views.update_profile_save, name='update_profile_save'),
    path('account_details', views.account_details, name='account_details'),
    path('transfer', views.transfer, name='transfer'),
    path('deposit_view', views.deposit_view, name='deposit_view'),
    path('withdrawal_view', views.withdrawal_view, name='withdrawal_view'),
    path('logout', views.logout, name='logout'),
]