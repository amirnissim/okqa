from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth import login, authenticate
from forms import RegistrationForm
from django.contrib.auth.models import Group, User

def create_user(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(username = form.cleaned_data['username'],
                                password = form.cleaned_data['password1'])
            login(request, user)
            return HttpResponseRedirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'create_user.html', { 'form': form, })

