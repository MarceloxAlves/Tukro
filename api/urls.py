from rest_framework import routers
from .views import PostagemViewSet

router = routers.SimpleRouter()
router.register(r'postagens', PostagemViewSet)
urlpatterns = router.urls
