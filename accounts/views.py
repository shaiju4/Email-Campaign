from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView

from .forms import UserRegistrationForm, UserLoginForm
from .services import create_user


def register_view(request: HttpRequest) -> HttpResponse:
    """
    Handle user registration.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered registration page or a redirect response.
    """
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = create_user(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"]
            )
            login(request, user)
            return redirect("campaign_list")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


class UserLoginView(LoginView):
    """
    Handle user login using built-in LoginView.
    
    """
    form_class = UserLoginForm
    template_name = "accounts/login.html"


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Log out the current user and redirect to the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirect response to the login page.
    """
    logout(request)
    return redirect("login")
