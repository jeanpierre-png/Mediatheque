from django.utils import timezone
from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404

from .models import Member, Media, Loan
from .forms import MediaForm
from .forms import MemberForm



def home(request):
    return render(request, 'home.html')


def member_list(request):
    members = Member.objects.all()
    return render(request, "member_list.html", {"members": members})


def create_member(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("member_list")
        else:
            form = MemberForm()
    return render(request, 'create_member.html', {"form": form})


def edit_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        member.firstname = request.POST["firstname"]
        member.lastname = request.POST["lastname"]
        member.email = request.POST["email"]
        member.save()
        return redirect("member_list")

    return render(request, "edit_member.html")


def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    member.delete()
    return redirect("member_list")


def media_list(request):
    medias = Media.objects.all()
    return render(request, "media_list.html", {"medias": medias})


def add_media(request):
    if request.method == "POST":
        form = MediaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("media_list")
        else:
            form = MemberForm()
        return render(request, "add_media.html", {"form": form})


def edit_media(request, pk):
    media = get_object_or_404(Media, pk=pk)

    if request.method == "POST":
        form = MediaForm(request.POST, instance=media)
        if form.is_valid():
            form.save()
            return redirect("media_list")
        else:
            form = MediaForm(instance=media)

        return render(request, "edit_media.html", {"form": form, "media": media})


def delete_media(request, pk):
    media = get_object_or_404(Media, pk=pk)

    if request.method == "POST":
        media.delete()
        return redirect("media_list")

    return render(request, "delete_media.html", {"media": media})


def loan_list(request, false=None):
    medias = Media.objects.flter(available=True,consultation_only=false)

    return render(request, "loan_list.html", {"medias": medias})


def create_loan(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    members = Member.objects.all()

    if request.method == "POST":
        member = get_object_or_404(Member, pk=request.POST["member"])

        if not media.available or media.consultation_only:
            messages.error(request, "Ce média ne peut pas être emprunté.")
            return  render(request,"create_loan.html", {"media": media, "members": members})

        Loan.objects.create(
            member=member,
            media=media,
            loan_date=timezone.now()
        )

        media.available = False
        media.save()

        messages.success(request, "Emprunt créé avec succès.")
        return redirect("member_list")

    return render(request, "create_loan.html", {"media": media, "members": members})


def return_loan(request, pk):
    loan = get_object_or_404(Loan, pk=pk)
    loan.return_date = timezone.now()
    loan.save()

    media = Loan.media
    media.available = True
    media.save()

    return redirect("media_list")


