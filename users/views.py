from django.db.models import fields
from django.db.models.base import Model
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegister,UserUpdate,ProfileUpdate
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = UserRegister(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account Created')
            return redirect('login')
    else:
         form = UserRegister()
    context = {
        "form": form
    }
    return render(request,'users/register.html', context=context)


@login_required
def profile(request):
    if request.method == 'POST':
        user_update = UserUpdate(request.POST,instance=request.user)
        profile_update = ProfileUpdate(request.POST, request.FILES, instance=request.user.profile)
        if user_update.is_valid() and profile_update.is_valid():
            user_update.save()
            profile_update.save()
            messages.success(request, f'Account has been updated!')
            return redirect('profile')
    else:   
        user_update = UserUpdate(instance=request.user)
        profile_update = ProfileUpdate(instance=request.user.profile)
    context = {
        'user_update': user_update,
        'profile_update': profile_update,
    }
    return render(request,'users/profile.html', context=context)




