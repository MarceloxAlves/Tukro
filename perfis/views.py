from django.shortcuts import render
from perfis.models import Perfil, Convite, Postagem
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.generic.base import View, TemplateView
from django.utils.safestring import mark_safe
from .forms import *
import json


# Create your views here.

class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        contexto = {
            'perfis': self.get_perfis(request),
            'postagens': request.user.perfil.get_postagens(),
            'hashtags': self.get_hashtags(),
            'privacidades': Postagem.PRIVACIDADES,
        }
        if request.user.is_superuser == True:
            self.template_name = 'index_admin.html'

        return render(request, self.template_name, contexto)

    def post(self, request):
        texto = request.POST["texto"]
        privacidade = request.POST["privacidade"]
        imagem = request.FILES.get("imagem", None)
        usuario = request.user
        postagem = Postagem(texto=texto, perfil=usuario.perfil, privacidade=privacidade, imagem=imagem)
        postagem.save()
        return redirect('index')

    def get_hashtags(self):
        return Hashtag.objects.all()

    def get_perfis(self, request):
        return Perfil.objects.all().exclude(usuario=get_perfil_logado(request))

    def get_postagens(self, request):
        return Postagem.objects.filter(perfil=request.user.perfil)


@login_required
def exibir_perfil(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    postagens = perfil.get_public_perfil()
    regra_convite = request.user.perfil.regras_convite(perfil)

    if not perfil in request.user.perfil.bloqueados.all():
        return render(request, 'perfil.html',
                  {'perfil': perfil,
                   'regra_convite': regra_convite,
                   'postagens': postagens})
    else:
        return redirect('index')


@login_required
def exibir_meu_perfil(request):
    perfil = Perfil.objects.get(id=request.user.perfil.id)
    postagens = Postagem.objects.filter(perfil=request.user.perfil.id)

    return render(request, 'meu_perfil.html',
                  {'perfil': perfil,
                   'postagens': postagens})


def bloquear_usuario(request, perfil_id):
    perfil = Perfil.objects.get(id=perfil_id)
    get_perfil_logado(request).perfil.bloquear(perfil)

    return redirect('index')


def desativar_perfil(request):
    usuario_logado = get_perfil_logado(request)
    usuario_logado.is_active = False
    usuario_logado.save()

    return redirect('index')


@login_required
def prover_rebaixar(request, id):
    perfil = Perfil.objects.get(id=id)
    if request.user.is_superuser:
        if not perfil.usuario.is_superuser:
            perfil.usuario.is_superuser = True
        else:
            perfil.usuario.is_superuser = False
        perfil.usuario.save()
    return redirect('exibir', perfil_id=id)


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


class BuscaAmigoView(TemplateView):
    def get(self, request):
        pesquisa = request.GET['q']
        resultado = Perfil.objects.filter(nome__contains=pesquisa)\
                                .exclude(usuario=request.user)\
                                .exclude(usuario__perfil__in=request.user.perfil.bloqueados.all())
        return render(request, self.template_name, {'resultado': resultado})
