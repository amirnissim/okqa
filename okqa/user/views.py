from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib import messages

from forms import *

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
    profile = user.get_profile()
    user.avatar_url = profile.avatar_url()
    user.bio = profile.bio
    user.url = profile.url

    # todo: support members as well as candidates
    return render(request, "user/candidate_detail.html", 
            {"user": user, "answers": answers})


@login_required
def edit_profile(request):
    profile = request.user.get_profile()
    if request.method == "POST":
        form = ProfileForm(request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(user.get_absolute_url())

        #TODO: make this better - show the form
        # return HttpResponseRedirect("/#question_modal")
    elif request.method == "GET":
        form = ProfileForm(request.user)
    return render(request, "user/edit_profile.html", {"form": form})
