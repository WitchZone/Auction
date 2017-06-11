from django.contrib import admin

from .models import Lot_sub
from .models import UserProfile

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Lot_sub)
