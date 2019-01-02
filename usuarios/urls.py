
from django.contrib import admin
from django.urls import path, include
from perfis import views
from usuarios.views import RegistrarUsuarioView, LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.conf.urls import url


urlpatterns = [
    path('', login_required(views.HomeView.as_view()), name='index'),
    path('registrar/', RegistrarUsuarioView.as_view(), name="registrar"),
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='login.html'), name="logout")

]


