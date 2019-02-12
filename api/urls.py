from rest_framework import routers
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.documentation import include_docs_urls

from .views import PostagemViewSet, PostagemReacao, PerfilViewSet, ContaViewSet, PostagemRecordsView, \
    ReactionTypeRecordsView

router = routers.SimpleRouter()
urlpatterns = [
    path('', include_docs_urls(title='Tukro')),
    path('token/', obtain_auth_token),
    path('postagens/', PostagemRecordsView.as_view(), name="postagem_list"),
    path('postagens/<int:pk>/delete', PostagemViewSet.as_view({'delete': 'destroy'}), name="postagem_delete"),
    path('postagens/<int:pk>/compartilhar', PostagemViewSet.as_view({'patch': 'compartilhar'}), name="postagem_compartilhar"),
    path('postagens/<int:pk>/reagir/<int:reaction>', PostagemReacao.as_view({'get': 'reagir'}), name="postagem_reagir"),
    path('perfil/alterar-imagem/', PerfilViewSet.as_view({'post': 'alterar_imagem'}), name="alterar_imagem"),
    path('perfil/desativar-conta/', PerfilViewSet.as_view({'post': 'desativar_conta'}), name="desativar_conta"),
    path('perfil/reativar-conta/', ContaViewSet.as_view({'post': 'reativar_conta'}), name="reativar_conta"),
    path('reactions/', ReactionTypeRecordsView.as_view(), name="reactions"),

]
urlpatterns += router.urls