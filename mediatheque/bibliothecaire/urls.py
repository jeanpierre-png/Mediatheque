from django.urls import path
from . import views


urlpatterns = [

    path("", views.bibliothecaire_home, name="bibliothecaire_home" ),

    path( "members/", views.member_list, name="member_list" ),
    path( "member/add/", views.create_member, name="create_member" ),
    path("member/edit/<int:member_id>/", views.edit_member, name="edit_member" ),
    path("member/delete/<int:member_id>/", views.delete_member, name="delete_member" ),

    path("medias/", views.media_list, name="media_list" ),
    path("media/add/", views.add_media, name="add_media" ),
    path("media/edit/<int:media_id>/", views.edit_media, name="edit_media" ),
    path("media/delete/<int:media_id>/", views.delete_media, name="delete_media" ),
    path("media/loan/<int:media_id>/", views.create_loan, name="create_loan" ),

    path("loans/", views.loan_list, name="loan_list" ),
    path("loan/<int:loan_id>/return", views.return_loan, name="return_loan" ),
]