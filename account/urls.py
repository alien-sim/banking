from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('profile-form', views.profile_form, name='profile-form'),
    path('profile_save', views.profile_save, name='profile_save'),
    path('transfer', views.transfer, name='transfer'),
    url(r'^confirm/(?P<activation_key>\w+)/$', views.signup_confirm,name='signup-confirm'),
    path('logout', views.logout, name='logout'),
]