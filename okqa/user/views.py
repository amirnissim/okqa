from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django import forms
from django.contrib import messages

def login(request):
    nxt = request.META['HTTP_REFERER'] if request.META['HTTP_REFERER'] else reverse('home')
    if request.method == "POST":
        user = request.user
        if user.is_authenticated():
            auth_logout(request)
        else:
            username = request.POST['username']
            password = request.POST['password']
            if '@' in username:
                try:
                    u = User.objects.get(email__iexact=username)
                    username=u.username
                except User.DoesNotExist:
                    messages.warning(request, _('Email not found'))
                    return HttpResponseRedirect(nxt)
                except:
                    messages.warning(request, _('Email lookup error, please file a bug'))
                    return HttpResponseRedirect(nxt)
            user = authenticate(username=username, password=password)
            if user is None:
                messages.warning(request, _('Incorrect Username/Password'))
            else:
                if user.is_active:
                    auth_login(request, user)
                else:
                    messages.warning(request, _('Account is inactive'))
    return HttpResponseRedirect(nxt)


