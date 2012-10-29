from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _
from django import forms
from django.contrib import messages

def login (request):
    if request.user.is_authenticated():
        return HttpResponseForbidden(_('You are already logged in'))

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user.is_active and user.check_password(form.cleaned_data['password']):
                auth_login(request, user)
                return HttpResponse()
        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseForbidden(_('You need to use POST to login'))


