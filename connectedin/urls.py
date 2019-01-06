"""connectedin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from perfis import views
from usuarios.views import RegistrarUsuarioView, LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('v1/', include('api.urls'), name='api'),
    path('perfil/', include('perfis.urls'), name='perfil'),
    path('', include('usuarios.urls'), name='usuario'),
    path('admin/', admin.site.urls),

    path('teste/', views.index, name="teste"),
    url(r'teste/(?P<room_name>[^/]+)/', views.room, name="room"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)