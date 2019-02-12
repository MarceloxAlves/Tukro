from django.contrib.auth.models import User
from rest_framework import serializers
from perfis.models import Postagem, Justificativa, Perfil, Hashtag, Partilhamento, Reaction, ReactionType


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'label',)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','email','is_superuser')

class ReactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ReactionType
        fields = '__all__'


class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    class Meta:
        model = Perfil
        fields = ('id','nome','imagem', 'usuario')


class PostagemPartilhamentoSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)
    data = serializers.DateTimeField(format="%d-%m-%Y %H:%M")

    class Meta:
        model = Postagem
        fields = ('id','data','texto','perfil', 'privacidade', 'imagem','tipo','total_reactions')

class PostagemSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    data = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    post_partilhamento =  PostagemPartilhamentoSerializer(read_only=True)

    class Meta:
        model = Postagem
        fields = ('id','data','texto','perfil', 'privacidade', 'imagem', 'hashtags', 'qtd_hashtags', 'tipo', 'post_partilhamento', 'total_reactions')

class PartilhamentoSerializer(serializers.ModelSerializer):
    perfil = PerfilSerializer(read_only=True)
    hashtags = HashtagSerializer(many=True, read_only=True)
    data = serializers.DateTimeField(format="%d-%m-%Y %H:%M")
    post = PostagemSerializer(read_only=True)

    class Meta:
        model = Partilhamento
        fields = ('id','data','texto','perfil', 'privacidade', 'imagem', 'hashtags', 'post','tipo', 'total_reactions')


class JustificativaSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Justificativa
        fields = ('data_bloqueio','texto')

