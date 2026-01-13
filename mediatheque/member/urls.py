from django.urls import path
from . import views

urlpatterns = [

    path("medias/", views.media_list, name="member_media_list"),
]