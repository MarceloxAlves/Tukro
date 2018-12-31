from django.conf.urls import url
from perfis import  consumers

websocket_urlpatterns = [
    url(r'^ws/postagem/(?P<room_name>[^/]+)/$', consumers.PostConsumer),
]

