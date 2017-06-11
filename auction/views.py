from django.shortcuts import render

# Create your views here.

def lot_list(request):
    return render(request, 'auction/index.html', {})