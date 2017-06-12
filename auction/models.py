from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Lot_sub(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    starting_price = models.PositiveIntegerField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    is_open = models.BooleanField(default=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    balance = models.BigIntegerField()

    def __str__(self):
        return self.user.username

class LotRate(models.Model):
    participant = models.ForeignKey('auth.User')
    lot_id = models.ForeignKey('Lot_sub')
    rate = models.PositiveIntegerField()

    def __str__(self):
        return self.lot_id
