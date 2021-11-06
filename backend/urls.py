from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Knowledge Center API",
        default_version='v1',
        description="Knowledge Center API Endpoints",
        contact=openapi.Contact(email="allwindicaprio@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include(('users.urls', 'user'), namespace='user')),
    path('base/', include(('core.urls', 'user'), namespace='knowledge-base')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]

# swagger endpoints
urlpatterns += [
    url('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]
