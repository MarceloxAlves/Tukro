from django.contrib.auth.models import User
from rest_framework import viewsets, status
from perfis.models import Postagem, Reaction, ReactionType, Justificativa
from .serializer import PostagemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response


class PostagemViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Postagem.objects.filter(perfil=request.user.perfil)
        serializer = PostagemSerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        postagem = Postagem.objects.get(id=pk)
        postagem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        authentication_classes = [SessionAuthentication]
        return [auth() for auth in authentication_classes]


class PostagemReacao(viewsets.ViewSet):

    def reagir(self, request, pk=None, reaction=None):
        perfil = request.user.perfil;
        postagem = Postagem.objects.get(id=pk)
        reactionType = ReactionType.objects.get(id=reaction)
        reacoes = Reaction.objects.filter(postagem=postagem, perfil=perfil)
        if (reacoes):
            if (reacoes[0].tipo == reactionType):
                reacoes[0].delete()
                reactionType = ReactionType.objects.get(id=1)
            else:
                reacoes[0].tipo = reactionType
                reacoes[0].save()
        else:
            reacao = Reaction(perfil=perfil, postagem=postagem, tipo=reactionType)
            reacao.save()

        total = postagem.reactions.count()

        return Response(status=status.HTTP_200_OK, data={
            "postagem": {
                "id": postagem.id
            },
            "tipo": {
                "icon": reactionType.icon,
                "color": reactionType.color,
                "label": reactionType.label,
            },
            'total': total
        })

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        authentication_classes = [SessionAuthentication]
        return [auth() for auth in authentication_classes]


class PerfilViewSet(viewsets.ViewSet):

    def alterar_imagem(self, request):
        user = request.user.perfil
        user.imagem = request.FILES['imagem']
        user.save()
        return Response(status=status.HTTP_200_OK, data={
            "perfil": {
                "imagem": {
                    "url": user.imagem.url
                }
            }
        })

    def desativar_conta(self, request):
        try:
            user = request.user
            justificativa = Justificativa(user=user, texto=request.data['texto'])
            justificativa.save()
            user.is_active = False;
            user.save();
            return Response(status=status.HTTP_200_OK, data={
                "msg": "usuario desativado"
            })
        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "erro": "Não foi possível desativar esta conta: " + str(ex)
            })

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        authentication_classes = [SessionAuthentication]
        return [auth() for auth in authentication_classes]


class ContaViewSet(viewsets.ViewSet):
    def reativar_conta(self, request):
        try:
            user = User.objects.get(id=request.data['user_id']);
            user.is_active = True
            user.save()
            return Response(status=status.HTTP_200_OK, data={
                "msg": "Conta ativada"
            })
        except Exception as ex:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "erro": "Não foi possível ativar esta conta: " + str(ex)
            })
    def get_permissions(self):
        permission_classes = []
        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        authentication_classes = []
        return [auth() for auth in authentication_classes]