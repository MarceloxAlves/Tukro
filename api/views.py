from rest_framework import viewsets, status
from perfis.models import Postagem, Reaction, ReactionType
from .serializer import PostagemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response


class PostagemViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Postagem.objects.filter(perfil=request.user.perfil)
        serializer = PostagemSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        pass

    def retrieve(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

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
        reacoes  =  Reaction.objects.filter(postagem=postagem, perfil=perfil)
        if(reacoes):
            if(reacoes[0].tipo == reactionType):
                reacoes[0].delete()
                reactionType = ReactionType.objects.get(id=1)
            else:
                reacoes[0].tipo =  reactionType
                reacoes[0].save()
        else:
            reacao = Reaction(perfil=perfil, postagem=postagem, tipo=reactionType)
            reacao.save()

        total = postagem.reactions.count()

        return Response(status=status.HTTP_200_OK, data={
            "postagem": {
                "id": postagem.id
            } ,
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
