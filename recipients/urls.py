from django.urls import path
from .views import upload_recipient,list_recipients

urlpatterns =[
    path("upload_recipient",upload_recipient,name="upload_recipient"),
    path("list_recipients",list_recipients,name="list_recipients"),
]
