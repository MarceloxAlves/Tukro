from rest_framework import routers
from django.urls import path
from .views import PostagemViewSet, PostagemReacao, PerfilViewSet, ContaViewSet, PostagemRecordsView

router = routers.SimpleRouter()
urlpatterns = [
    path('postagens/', PostagemRecordsView.as_view(), name="postagem_list"),
    path('postagens/<int:pk>/delete', PostagemViewSet.as_view({'delete': 'destroy'}), name="postagem_delete"),
    path('postagens/<int:pk>/reagir/<int:reaction>', PostagemReacao.as_view({'get': 'reagir'}), name="postagem_reagir"),
    path('perfil/alterar-imagem/', PerfilViewSet.as_view({'post': 'alterar_imagem'}), name="alterar_imagem"),
    path('perfil/desativar-conta/', PerfilViewSet.as_view({'post': 'desativar_conta'}), name="desativar_conta"),
    path('perfil/reativar-conta/', ContaViewSet.as_view({'post': 'reativar_conta'}), name="reativar_conta"),

]
urlpatterns += router.urls