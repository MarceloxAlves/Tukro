from rest_framework import routers
from django.urls import path
from .views import PostagemViewSet, PostagemReacao, PerfilViewSet

router = routers.SimpleRouter()
urlpatterns = [
    path('postagens/', PostagemViewSet.as_view({'get': 'list'}), name="postagem_list"),
    path('postagens/<int:pk>/delete', PostagemViewSet.as_view({'delete': 'destroy'}), name="postagem_delete"),
    path('postagens/<int:pk>/reagir/<int:reaction>', PostagemReacao.as_view({'get': 'reagir'}), name="postagem_reagir"),
    path('perfil/alterar-imagem/', PerfilViewSet.as_view({'post': 'alterar_imagem'}), name="alterar_imagem"),

]
urlpatterns += router.urls