from django.urls import path
from django.views.generic import TemplateView
from modules.accounts.views import (
    AccountActivationViewSet,
    GoogleSocialLogin,
    LoginViewSet,
    PasswordResetTokenCheckViewSet,
    RefreshViewSet,
    RegisterViewSet,
    RequestPasswordResetPhoneNumber,
    SetNewPasswordViewSet,
)
from modules.store.views import (
    AuthorViewSet,
    BookViewSet,
    GenreViewSet,
    PublisherViewSet,
)
from rest_framework.routers import SimpleRouter

app_name = "api"
routes = SimpleRouter()


# accounts
routes.register("login", LoginViewSet, basename="login")
routes.register("register", RegisterViewSet, basename="register")
routes.register("auth/refresh", RefreshViewSet, basename="authRefresh")
routes.register("activate", AccountActivationViewSet, basename="activate")
routes.register(
    "password-reset",
    RequestPasswordResetPhoneNumber,
    basename="requestPasswordResetPhoneNumber",
)
routes.register(
    "password-reset-token-check",
    PasswordResetTokenCheckViewSet,
    basename="passwordResetTokenCheck",
)
routes.register(
    "password-reset-complete", SetNewPasswordViewSet, basename="password-reset-complete"
)
routes.register("google/login", GoogleSocialLogin, basename="googleLogin")

# store
routes.register("authors", AuthorViewSet, basename="authors")
routes.register("genres", GenreViewSet, basename="genres")
routes.register("publishers", PublisherViewSet, basename="publishers")
routes.register("books", BookViewSet, basename="books")
urlpatterns = [
    *routes.urls,
]
