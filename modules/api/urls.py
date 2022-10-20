from django.urls import path
from django.views.generic import TemplateView
from rest_framework.routers import SimpleRouter


app_name = "api"
routes = SimpleRouter()

urlpatterns = [
    *routes.urls,
]
