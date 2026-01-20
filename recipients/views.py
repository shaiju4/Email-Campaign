import logging

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required,user_passes_test

from .forms import RecipientForm
from .services import bulk_upload_recipients
from .models import Recipient
from accounts.permission import is_admin


logger = logging.getLogger(__name__)

@login_required
@user_passes_test(is_admin)
def upload_recipient(request: HttpRequest) -> HttpResponse:
    """
    Handle bulk upload of recipients by an admin user.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        HttpResponse: Redirects to the recipient list page after processing
        a POST request, or renders the upload form for GET requests.
    """
    if request.method == "POST":
        form = RecipientForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                count = bulk_upload_recipients(request.FILES['file'],request.user)
                logger.info(f"{count} recipients uploaded.")
                return redirect("list_recipients")   
            except Exception as e:
                logger.error(f"Failed to upload recipients : {e}")
                form.add_error(
                    None,
                    str(e) or "Failed to upload recipients."
                )
        return render(
            request,
            "recipient/upload.html",
            {"form": form},
        )
    
    form = RecipientForm()
    return render(request, "recipient/upload.html", {"form": form})

@login_required
@user_passes_test(is_admin)
def list_recipients(request: HttpRequest) -> HttpResponse:
    """
    Display a list of all recipients for admin users.

    Args:
        request (HttpRequest): The incoming HTTP request object.

    Returns:
        HttpResponse: Renders the recipient list template with
        all available recipients.
    """
    try:
        recipients = Recipient.objects.all()
        logger.info(f"{len(recipients)} recipients fetched.")
    except Exception as e:
        logger.error(f"Failed to fetch recipients list: {e}")
        recipients = []
    return render(request, "recipient/recipient_list.html", {"recipients": recipients})
