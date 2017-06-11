from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Lot_sub
from .forms import UserForm, UserProfileForm, LotForm
from .models import UserProfile

# Create your views here.

def lot_list(request):
    lots = Lot_sub.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'auction/lot.html', {'lots': lots})

def lot_detail(request, pk):
        lot = get_object_or_404(Lot_sub, pk=pk)
        return render(request, 'auction/lot_detail.html', {'lot': lot})

@login_required
def lot_edit(request, pk):
        post = get_object_or_404(Lot_sub, pk=pk)
        if request.method == "POST":
            form = LotForm(request.POST, instance=post)
            if form.is_valid():
                lot = form.save(commit=False)
                lot.author = request.user
                lot.published_date = timezone.now()
                lot.save()
                return redirect('lot_detail', pk=lot.pk)
        else:
            form = LotForm(instance=post)
        return render(request, 'auction/lot_edit.html', {'form': form})

@login_required
def lot_new(request):
        if request.method == "POST":
            form = LotForm(request.POST)
            if form.is_valid():
                lot = form.save(commit=False)
                lot.author = request.user
                lot.published_date = timezone.now()
                lot.save()
                return redirect('lot_detail', pk=lot.pk)
        else:
            form = LotForm()
        return render(request, 'auction/lot_edit.html', {'form': form})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm()

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'auction/register.html',
                  {'user_form': user_form,
                   'profile_form': profile_form,
                   'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('lot_list'))
        else:
            print('Invalid login details: {0}, {1}'.format(username, password))
            return HttpResponse('Invalid login details')
    else:
        return render(request, 'auction/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('lot_list'))