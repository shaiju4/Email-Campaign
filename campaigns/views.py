import logging

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required,user_passes_test

from .forms import CampaignForm
from .models import Campaign
from accounts.permission import is_admin

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
@login_required
@user_passes_test(is_admin)
def create_campaign(request: HttpRequest) -> HttpResponse:
    """
    Create a new email campaign.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse:
            - Redirects to the campaign list view upon successful creation.
            - Renders the campaign creation template with form errors
              if validation fails or an exception occurs.
    """
    form = CampaignForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        try:
            campaign = form.save()

            logger.info(
                "Campaign created successfully | campaign_id=%s name=%s",
                campaign.id,
                campaign.name,
            )
            return redirect("campaign_list")
        except Exception:
            logger.exception(
                "Unexpected error while creating campaign"
            )
            form.add_error(
                None,
                "An unexpected error occurred while creating the campaign."
            )
    return render(
        request,
        "campaigns/create_campaign.html",
        {"form": form},
    )


@require_http_methods(["GET"])
@login_required
def campaign_list(request: HttpRequest) -> HttpResponse:
    """
    Display a list of all email campaigns.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse:
            Renders the campaign list template populated with
            all available campaigns.
    """
    campaigns = Campaign.objects.order_by("-created_at")
    return render(
        request,
        "campaigns/campaign_list.html",
        {"campaigns": campaigns},
    )


@require_http_methods(["GET"])
@login_required
@user_passes_test(is_admin)
def campaign_detail(request: HttpRequest, campaign_id: int) -> HttpResponse:
    """
    Display detailed information for a single campaign.

    Args:
        request (HttpRequest): The incoming HTTP request.
        campaign_id (int): The unique identifier of the campaign.

    Returns:
        HttpResponse:
            Renders the campaign detail template containing the
            campaign information and its related email delivery logs.

    Raises:
        Http404: If the campaign with the given ID does not exist.
    """

    campaign = get_object_or_404(Campaign, id=campaign_id)
    email_logs = campaign.email_logs.all().order_by("-created_at")
    return render(
        request,
        "campaigns/campaign_detail.html",
        {
            "campaign": campaign,
            "email_logs": email_logs,
        },
    )
    
@login_required
def campaign_list_status_api(request:HttpRequest):
    """
    Return the current status and counts for all campaigns.
    
    Args:
        request (HttpRequest): The incoming HTTP request.
    
    """
    campaigns = Campaign.objects.values(
        "id",
        "status",
        "sent_count",
        "failed_count",
    )

    return JsonResponse(
        {"campaigns": list(campaigns)},
        safe=False
    )
