from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django import forms
from django.contrib import messages


