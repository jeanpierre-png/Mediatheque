from django import forms
from .models import Member, Media, Loan

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ["firstname", "lastname", "email"]

        labels = {
            "firstname": "Prénom",
            "lastname": "Nom",
            "email": "Email",
        }

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ["title", "media_type", "author", "artist", "realisator", "creator"]

        labels = {
            "title": "Titre",
            "media_type" : "Type de média",
            "author": "Auteur",
            "artist": "Artiste",
            "realisator": "Réalisateur",
            "creator": "Créateur",
            "available": "Disponible",
        }


class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        fields = ["member", "media"]

        labels = {
            "member": "Membre",
            "media": "Media",
        }