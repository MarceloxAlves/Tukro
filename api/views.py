from rest_framework import viewsets, status
from perfis.models import Postagem
from .serializer import PostagemSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response


class PostagemViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Postagem.objects.filter(perfil = request.user.perfil)
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
        postagem =  Postagem.objects.get(id=pk)
        postagem.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_permissions(self):
        permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_authenticators(self):
        authentication_classes = [SessionAuthentication]
        return [auth() for auth in authentication_classes]
