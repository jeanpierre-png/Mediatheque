from datetime import timedelta
from django.db import models
from django.utils import timezone


class Member(models.Model):

    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    joined_date = models.DateField(default=timezone.now)

    def current_loans_count(self):
        return self.active_loans().count()

    def active_loans(self):
        return self.loan_set.filter(return_date__isnull=True)
    
    def has_late_loan(self):
        return any(loan.is_late() for loan in self.active_loans())
    
    def has_too_many_loans(self):
        return self.current_loans_count() >= 3
    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Media(models.Model):

    TYPES_MEDIA =[
        ('books', 'Livre'),
        ('cds', 'CD'),
        ('dvds', 'DVD'),
        ('game', 'Jeux De Plateau'),
    ]

    title = models.CharField(max_length=200)
    media_type = models.CharField(max_length=50, choices=TYPES_MEDIA)

    available = models.BooleanField(default=True)
    consultation_only = models.BooleanField(default=False)

    author = models.CharField(max_length=100, blank=True, null=True) # Livre
    artist = models.CharField(max_length=100, blank=True, null=True) # Cd
    realisator = models.CharField(max_length=100, blank=True, null=True) # Dvd
    creator = models.CharField(max_length=100, blank=True, null=True) # Jeu de plateau

    def save(self, *args, **kwargs):

        self.author = None
        self.artist = None
        self.realisator = None
        self.creator = None

        if self.media_type == "game":
            self.consultation_only = True
            self.available = True
        else:
            self.consultation_only = False
            self.available = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.media_type})"


class Loan(models.Model):

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    loan_date = models.DateField(default=timezone.now)
    return_date = models.DateField(null=True, blank=True)
    
    def due_date(self):
        return self.loan_date + timedelta(days=7)
    
    def is_late(self):
        return self.return_date is None and timezone.now().date() > self.due_date()
    
    def is_return(self):
        return self.return_date is not None
    
    def __str__(self):
        return f"{self.member} → {self.media}"
