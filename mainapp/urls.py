from django.urls import path
from django.contrib import auth
from . import views
from django.contrib.auth import views as auth
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('', views.Home, name='Home'),
    path('terms_&_conditions/', views.tac, name='tac'),
    path('privacy_policy/', views.pp, name='pp'),
    path('disclaimer/', views.dis, name='dis'),


    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('assets/favicon.ico'))),


    path('register/', views.register, name ='register'),
    path('login/', views.Login, name ='login'),
    path('logout/', views.Logout, name ='logout'),
    path('userauth/', views.UserAuthform, name='UserAuthForm'),
    path('userauthemail/', views.UserAuthemail, name='UserAuthEmail'),
    path('edit_profile/', views.EditProfile, name='edit_profile'),
    path('forget_pass/', views.Forgetpass, name='forgetpass'),
    path('reset_pass/<token>/', views.ChangePass, name='changepass'),


    path('aboutus/', views.AboutUs, name='aboutus'),
    path('contactus/', views.ContactUs, name='contactus'),
    path('donate/', views.Donate, name='donate'),


    path('bot/', views.Bot, name='bot'),
    path('bot/<str:pk>', views.TypeBot, name='typebot'),
    path('pmembership/', views.Pmembership, name='pmembership'),


    path('help/find_auth/', views.AuthHelp, name='authhelp'),
]

handler404 = 'mainapp.views.Error_404'