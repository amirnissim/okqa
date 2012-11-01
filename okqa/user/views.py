from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _
from django import forms
from django.contrib import messages

# TODO: move to settings
CANDIDATES_GROUP_NAME = "candidates"
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

def candidate_list(request):
    """
    list candidates ordered by number of answers
    """
    g = Group.objects.get(name=CANDIDATES_GROUP_NAME)
    candidates = g.user_set.all().annotate(num_answers=Count('answers')).order_by("-num_answers")
    return render(request, "user/candidate_list.html", {"candidates": candidates})


def user_detail(request, slug):
    user = get_object_or_404(User, username=slug)
    answers = user.answers.all()
    # todo: support members as well as candidates
    return render(request, "user/candidate_detail.html", 
            {"user": user, "answers": answers})


