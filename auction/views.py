from django.shortcuts import render
from django.utils import timezone
from .models import Lot_sub

# Create your views here.

def lot_list(request):
    lots = Lot_sub.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'auction/index.html', {'lots': lots})