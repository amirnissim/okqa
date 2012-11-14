from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.models import get_current_site
from django.conf import settings

from haystack.forms import SearchForm

from .models import *

def forms(request):
    context = {"search_form": SearchForm()}
    if not request.user.is_authenticated():
        context["login_form"] = AuthenticationForm()
    context["party"], created = Party.objects.get_or_create(site=get_current_site(request))
    context["ANALYTICS_ID"] = getattr(settings, 'ANALYTICS_ID', False)
    return context


