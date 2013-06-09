from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.contrib import messages

from .forms import *
from .models import *

def candidate_list(request):
    """
    list candidates ordered by number of answers
    """
    candidates = Profile.objects.candidates()
    return render(request, "user/candidate_list.html", {"candidates": candidates})

def user_detail(request, slug):
    user = get_object_or_404(User, username=slug)
    questions = user.questions.all()
    answers = user.answers.all()
    profile = user.profile
    user.avatar_url = profile.avatar_url()
    user.bio = profile.bio
    user.url = profile.url

    # todo: support members as well as candidates
    return render(request, "user/candidate_detail.html", 
            {"candidate": user, "answers": answers, "questions": questions})

@login_required
def edit_profile(request):
    profile = request.user.profile
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
