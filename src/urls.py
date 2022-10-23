from distutils.debug import DEBUG
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view  # new
from rest_framework import permissions  # new
from rest_framework.documentation import include_docs_urls


schema_view = get_schema_view(
    openapi.Info(
        title="The Narabell API",
        default_version="v1",
        description="African Tales Narrated",
        terms_of_service="https://coderpass.herokuapp.com",
        contact=openapi.Contact(email="deverbout@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
API_TITLE = "Narabell"
API_DESCRIPTION = "African Tales Naratted"


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("modules.api.urls")),
    path(
        "api/v1/docs/",
        include_docs_urls(
            title=API_TITLE,
            description=API_DESCRIPTION,
        ),
    ),
    path(
        "",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
