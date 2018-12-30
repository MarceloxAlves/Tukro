from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.views.generic.base import View, TemplateView
from perfis.models import Perfil
from usuarios.forms import RegistrarUsuarioForm


class RegistrarUsuarioView(View):
    template_name = 'registrar.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrarUsuarioForm(request.POST)
        if form.is_valid():
            dados_form = form.cleaned_data
            usuario = User.objects.create_user(username=dados_form['email'],
                                               password=dados_form['senha'],
                                               email=dados_form['email'])
            perfil = Perfil(nome=dados_form['nome'],
                            telefone=dados_form['telefone'],
                            nome_empresa=dados_form['nome_empresa'],
                            usuario=usuario)
            perfil.save()
            return redirect('index')
        return render(request, self.template_name, {'form': form})


class LoginView(TemplateView):
    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        print(user)
        if user is not None:
            login(request, user=user)
            return redirect('index')
        return render(request, self.template_name)


class LogoutView(TemplateView):
    def get(self, request):
        logout(request)
        return render(request, self.template_name)

    def post(self, request):
        logout(request)
        return render(request, self.template_name)
