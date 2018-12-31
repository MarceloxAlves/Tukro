from rest_framework import viewsets
from perfis.models import Postagem
from .serializer import PostagemSerializer
from rest_framework.permissions import IsAuthenticated

class PostagemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Postagem.objects.all()
    serializer_class = PostagemSerializer