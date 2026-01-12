from django.utils import timezone
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Member, Media, Loan
from .forms import MediaForm
from .forms import MemberForm



def home(request):
    return render(request, 'home.html')

def bibliothecaire_home(request):
    return render(request, 'pages/base_bibliothecaire.html')


def member_list(request):
    members = Member.objects.all()
    return render(request, "pages/member_list.html", {"members": members})


def create_member(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("member_list")
    else:
        form = MemberForm()

    return render(request, 'pages/create_member.html', {"form": form})


def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == "POST":
        member.firstname = request.POST["firstname"]
        member.lastname = request.POST["lastname"]
        member.email = request.POST["email"]
        member.save()
        return redirect("member_list")

    return render(request, "pages/edit_member.html", {"member": member})


def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)

    if request.method == "POST":
        member.delete()
        return redirect("member_list")

    return render(request, "pages/delete_member.html", {"member": member})


def media_list(request):
    medias = Media.objects.all()
    return render(request, "pages/media_list.html", {"medias": medias})


def add_media(request):

    if request.method == "POST":
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("media_list")
    else:
        form = MediaForm()

    return render(request, "pages/media_form.html", {"form": form})

from django.contrib import messages

def edit_media(request, media_id):
    media = get_object_or_404(Media, id=media_id)

    if request.method == "POST":
        form = MediaForm(request.POST, instance=media)
        if form.is_valid():
            form.save()
            return redirect("media_list")
    else:
        form = MediaForm(instance=media)

    return render(request, "pages/edit_media.html", {"form": form, "media": media})


def delete_media(request, media_id):

    media = get_object_or_404(Media, id=media_id)

    if request.method == "POST":
        media.delete()
        return redirect("media_list")

    return render(request, "pages/delete_media.html", {"media": media})


def loan_list(request):
    loans = Loan.objects.filter(return_date__isnull=True)
    medias = Media.objects.filter(
        available=True,
        consultation_only=False
    )
    return render(request, "pages/loan_list.html", {"loans": loans})


def create_loan(request, media_id):
    media = get_object_or_404(Media, id=media_id)
    members = Member.objects.all()

    if request.method == "POST":
        member_id = request.POST["member_id"]
        member = get_object_or_404(Member, id=member_id)

        if not media.available or media.consultation_only:
            messages.error(request, "Ce média ne peut pas être emprunté.")
            return redirect("media_list")

        Loan.objects.create(
            member=member,
            media=media,
            loan_date=timezone.now()
        )

        media.available = False
        media.save()

        messages.success(request, "Emprunt créé avec succès.")
        return redirect("member_list")

    return render(request, "pages/create_loan.html", {"media": media, "members": members})


def return_loan(request, loan_id):

    loan = get_object_or_404(Loan, id=loan_id)
    loan.return_date = timezone.now()
    loan.save()

    media = Loan.media
    media.available = True
    media.save()

    return redirect("media_list")


