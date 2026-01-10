from django.db import models


class Member(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)


class Media(models.Model):
    TYPES_MEDIA =[
        ('book', 'livre'),
        ('cds', 'Cd'),
        ('DVD', 'Dvd'),
        ('Game', 'Jeu de plateau'),
    ]

    title = models.CharField(max_length=100)
    media_type = models.CharField(max_length=100, choices=TYPES_MEDIA)

    available = models.BooleanField(default=True)
    consultation_only = models.BooleanField(default=False)

    author = models.CharField(max_length=100, blank=True, null=True) # Livre
    artist = models.CharField(max_length=100, blank=True, null=True) # Cd
    realisator = models.CharField(max_length=100, blank=True, null=True) # Dvd
    creator = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.media_type == "Game":
            self.consultation_only = True
            self.available = True
            super().save(*args, **kwargs)


class Loan(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    media = models.ForeignKey(Media, on_delete=models.CASCADE)
    loan_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
