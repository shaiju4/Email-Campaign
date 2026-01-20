from django.urls import path
from .views import register_view, logout_view, UserLoginView

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
