from rest_framework import serializers
from perfis.models import Postagem

class PostagemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Postagem
        fields = ('data','texto','perfil')
