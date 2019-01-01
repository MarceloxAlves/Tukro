from rest_framework import routers
from django.urls import path
from .views import PostagemViewSet

router = routers.SimpleRouter()
urlpatterns = [
    path('postagens/', PostagemViewSet.as_view({'get': 'list'}), name="postagem_list"),
    path('postagens/<int:pk>/delete', PostagemViewSet.as_view({'delete': 'destroy'}), name="postagem_delete"),
]
urlpatterns += router.urls