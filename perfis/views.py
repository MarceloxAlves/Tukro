from django.shortcuts import render
from perfis.models import Perfil, Convite, Postagem
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View, TemplateView
from django.utils.safestring import mark_safe
import json


# Create your views here.

class HomeView(View):
    template_name = 'index.html'
    def get(self, request):
        contexto = {
            'perfis': self.get_perfis(),
            'postagens': self.get_postagens(request),
        }
        return render(request, self.template_name,contexto)

    def post(self, request):
        texto = request.POST["texto"];
        usuario = request.user
        print(usuario)
        postagem = Postagem(texto=texto, perfil=usuario.perfil)
        postagem.save()
        contexto = {
            'perfis': self.get_perfis(),
            'postagens': self.get_postagens(request),
        }
        return render(request, self.template_name, contexto)

    def get_perfis(self):
        return Perfil.objects.all();

    def get_postagens(self, request):
        return Postagem.objects.filter(perfil=request.user.perfil);


@login_required
def exibir_perfil(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    postagens = Postagem.objects.filter(perfil=perfil_id)

    return render(request, 'perfil.html',
                  {'perfil': perfil,
                   'postagens': postagens})


@login_required
def exibir_meu_perfil(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    postagens = Postagem.objects.filter(perfil=perfil_id)

    return render(request, 'meu_perfil.html',
                  {'perfil': perfil,
                   'postagens': postagens})


@login_required
def convidar(request, perfil_id):
    perfil_a_convidar = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request).perfil

    if (perfil_logado.pode_convidar(perfil_a_convidar)):
        perfil_logado.convidar(perfil_a_convidar)

    return redirect('index')


@login_required
def desfazer_amizade(request, perfil_id):
    perfil_a_desfazer = Perfil.objects.get(id=perfil_id)
    perfil_logado = get_perfil_logado(request).perfil

    perfil_logado.desfazer_amizade(perfil_a_desfazer)

    return redirect('index')


@login_required
def get_perfil_logado(request):
    return request.user


@login_required
def aceitar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.aceitar()
    return redirect('index')


@login_required
def recusar(request, convite_id):
    convite = Convite.objects.get(id=convite_id)
    convite.recusar()
    return redirect('index');


def index(request):
    return render(request, 'teste/index.html', {})

def room(request, room_name):
    return render(request, 'teste/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })
