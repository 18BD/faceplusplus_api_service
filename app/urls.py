from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

import faces.urls


schema_view = get_schema_view(
    openapi.Info(
        title="Faces API",
        default_version='v1',
        description="",
    ),
    public=True,
    permission_classes=(),
)


urlpatterns = [
    path('api/v1/', include(faces.urls)),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # adds nothing if not in DEBUG
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # adds nothing if not in DEBUG
