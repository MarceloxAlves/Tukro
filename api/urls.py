from rest_framework import routers
from django.urls import path
from .views import PostagemViewSet, PostagemReacao

router = routers.SimpleRouter()
urlpatterns = [
    path('postagens/', PostagemViewSet.as_view({'get': 'list'}), name="postagem_list"),
    path('postagens/<int:pk>/delete', PostagemViewSet.as_view({'delete': 'destroy'}), name="postagem_delete"),
    path('postagens/<int:pk>/reagir/<int:reaction>', PostagemReacao.as_view({'get': 'reagir'}), name="postagem_reagir"),
]
urlpatterns += router.urls