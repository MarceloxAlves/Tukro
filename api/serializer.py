from django.contrib.auth.models import User
from rest_framework import serializers
from perfis.models import Postagem, Justificativa, Perfil


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','is_superuser')


class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    class Meta:
        model = Perfil
        fields = ('id','nome','imagem', 'usuario')

class PostagemSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)

    class Meta:
        model = Postagem
        fields = ('data','texto','perfil', 'privacidade', 'imagem')


class JustificativaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Justificativa
        fields = ('data_bloqueio','texto')

