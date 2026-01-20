from django.urls import path
from .views import create_campaign,campaign_list,campaign_detail,campaign_list_status_api

urlpatterns = [
    path("create_campaign/",create_campaign,name = "create_campaign"),
    path("",campaign_list,name = "campaign_list"),
    path(
        "campaigns/<int:campaign_id>/",
        campaign_detail,
        name="campaign_detail"
    ),
    path(
    "campaigns/status/",
    campaign_list_status_api,
    name="campaign_list_status_api",
),


]

