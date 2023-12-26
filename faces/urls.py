from rest_framework import routers

from .views import FaceViewSet


router = routers.SimpleRouter()
router.register('faces', FaceViewSet, basename='faces')

urlpatterns = [
    *router.urls,
]