from rest_framework import serializers
from perfis.models import Postagem, Justificativa


class PostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Postagem
        fields = ('data','texto','perfil')

class Justificativa(serializers.ModelSerializer):
    class Meta:
        model  = Justificativa
        fields = ('data_bloqueio','texto')
