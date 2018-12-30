from django.shortcuts import render
from perfis.models import Perfil, Convite
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
	return render(request, 'index.html',{'perfis' : Perfil.objects.all()})
@login_required
def exibir_perfil(request, perfil_id):

	perfil = Perfil.objects.get(id=perfil_id)

	return render(request, 'perfil.html',
		          {'perfil' : perfil, 
				   'perfil_logado' : get_perfil_logado(request)})
@login_required
def convidar(request,perfil_id):

	perfil_a_convidar = Perfil.objects.get(id=perfil_id)
	perfil_logado = get_perfil_logado(request)
	
	if(perfil_logado.pode_convidar(perfil_a_convidar)):
		perfil_logado.convidar(perfil_a_convidar)
	
	return  redirect('index')

@login_required
def get_perfil_logado(request):
	return Perfil.objects.get(id = 1)

@login_required
def aceitar(request, convite_id):
	convite = Convite.objects.get(id = convite_id)
	convite.aceitar()
	return redirect('index')


