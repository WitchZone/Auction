from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Lot_sub(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    starting_price = models.BigIntegerField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    end_date = models.DateTimeField(
            blank=True, null=True)

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