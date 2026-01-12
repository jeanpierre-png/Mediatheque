from django.db import models
from django.utils import timezone


class Member(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Media(models.Model):
    TYPES_MEDIA =[
        ('books', 'Livre'),
        ('cds', 'CD'),
        ('dvds', 'DVD'),
        ('game', 'Jeux De Plateau'),
    ]

    title = models.CharField(max_length=100)
    media_type = models.CharField(max_length=50, choices=TYPES_MEDIA)

    available = models.BooleanField(default=True)
    consultation_only = models.BooleanField(default=False)

    author = models.CharField(max_length=100, blank=True, null=True) # Livre
    artist = models.CharField(max_length=100, blank=True, null=True) # Cd
    realisator = models.CharField(max_length=100, blank=True, null=True) # Dvd
    creator = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.media_type == "game":
            self.consultation_only = True
            self.available = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.media_type})"


class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    loan_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
