from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from .models import Lot_sub
from .forms import UserForm, UserProfileForm, LotForm, RateForm, WinnerForm
from .models import UserProfile, Lot_sub, LotRate, Winner

# Create your views here.
def lot_list(request):
    lots = Lot_sub.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    return render(request, 'auction/lot.html', {'lots': lots})

def lot_detail(request, pk):
        lot = get_object_or_404(Lot_sub, pk=pk)
        user = request.user
        date_now = timezone.now()
        start_p = Lot_sub.objects.filter(pk=pk).values('starting_price')[0]['starting_price']
        mess = ""
        backers_list = LotRate.objects.filter(lot_id=lot).order_by('-rate')[:10]
        win = Winner.objects.filter(lot_id=lot)
        if (lot.author == user):
            ed = True
        else:
            ed = False
        if request.method == "POST":
            button_name = request.POST.get('submit')
            if button_name == "Rate":
                print("--==I went through button Rate==--")
                form = RateForm(request.POST);
                if form.is_valid():
                    rate_lot = form.save(commit=False)
                    bal = UserProfile.objects.filter(pk=user.id).values('balance')[0]['balance']
                    if rate_lot.rate > start_p and bal >= rate_lot.rate:
                        rate_lot.participant = user
                        print(rate_lot.participant)
                        rate_lot.lot_id = lot
                        rate_lot.save()
                        Lot_sub.objects.filter(pk=pk).update(starting_price=rate_lot.rate)
                        return redirect('lot_detail', pk=lot.pk)
                    elif bal < rate_lot.rate:
                        mess = "You do not have enough tokens"
                        return render(request, 'auction/lot_detail.html', {'lot': lot, 'ed': ed, 'date_now': date_now, 'form': form, 'mess': mess, 'backers_list': backers_list, 'win': win})
                    else:
                        mess = "The rate must be greater than the current price"
                        return render(request, 'auction/lot_detail.html', {'lot': lot, 'ed': ed, 'date_now': date_now, 'form': form, 'mess': mess, 'backers_list': backers_list, 'win': win})
            elif button_name == "Sold lot":
                print('--==I went through button Sold lot==--')
                bal = UserProfile.objects.filter(pk=user.id).values('balance')[0]['balance']
                check_sold = False
                for backer in backers_list:
                    bal_curr = UserProfile.objects.filter(user=backer.participant).values('balance')[0]['balance']
                    if bal_curr > backer.rate:
                        print('Sold by', backer.participant, ' behind', backer.rate, 'tokens')
                        new_bal_curr = bal_curr - backer.rate
                        new_bal = bal + backer.rate
                        
                        UserProfile.objects.filter(user=user.id).update(balance=new_bal)
                        UserProfile.objects.filter(user=backer.participant).update(balance=new_bal_curr)
                        Winner.objects.filter(lot_id=lot).update(winner=backer.participant)
                        Lot_sub.objects.filter(pk=pk).update(is_open=False)
                        return redirect('lot_detail', pk=lot.pk)
                    else:
                        print('--==',backer.participant, ' does not have tokens==--')
                if check_sold == False:
                    print('--==No one can redeem==--')
                    mess = "Users without tokens, or no one paid"
                    form = RateForm()
                    
            else:
                print('--==How did I even find myself here?==--')
                return redirect('lot_detail', pk=lot.pk)
        else:
            form = RateForm()
        return render(request, 'auction/lot_detail.html', {'lot': lot, 'ed': ed, 'date_now': date_now, 'form': form, 'mess': mess, 'backers_list': backers_list, 'win': win })

@login_required
def lot_edit(request, pk):
        lot = get_object_or_404(Lot_sub, pk=pk)
        if request.method == "POST":
            form = LotForm(request.POST, instance=lot)
            if form.is_valid():
                lot = form.save(commit=False)
                lot.author = request.user
                lot.published_date = timezone.now()
                lot.save()
                return redirect('lot_detail', pk=lot.pk)
        else:
            form = LotForm(instance=lot)
            if (lot.author == request.user):
                ed = True
            else:
                ed = False
        return render(request, 'auction/lot_edit.html', {'form': form, 'ed': ed})

@login_required
def lot_remove(request, pk):
    lot = get_object_or_404(Lot_sub, pk=pk)
    lot.delete()
    return redirect('lot_list')

@login_required
def user_balance(request):
    user = request.user
    bal = UserProfile.objects.filter(pk=user.id).values('balance')[0]['balance']
    if request.method == "POST":
        balance = int(request.POST.get('balance'))
        new_bal = bal + balance
        UserProfile.objects.filter(pk=user.id).update(balance=new_bal)
        return HttpResponseRedirect(reverse('balance'))
    return render(request, 'auction/balance.html', {'bal': bal})

@login_required
def lot_new(request):
        if request.method == "POST":
            winnerform = WinnerForm()
            form = LotForm(request.POST)
            if form.is_valid():
                lot = form.save(commit=False)
                lot.author = request.user
                lot.published_date = timezone.now()
                lot.save()

                win = winnerform.save(commit=False)
                win.winner = request.user
                win.lot_id = lot
                win.save()
                return redirect('lot_detail', pk=lot.pk)
        else:
            form = LotForm()
            ed = True
        return render(request, 'auction/lot_edit.html', {'form': form, 'ed': ed})

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
            profile.balance = 5;
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
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'auction/login.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('lot_list'))


def get_au_views(request):
    if request.method == 'POST':
        lot_id = request.get('lot_id')
        lot = Lot_sub.get(pk=lot_id)
        lot.views += 1
        lot.save()
        response = {}
        return HttpResponse(
            json.dumps(response),
            content_type='application/json'
        )
