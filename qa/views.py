from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth import login, authenticate
from qa.models import Question
from forms import RegistrationForm


def create_question(request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    subject = request.POST.get("subject")
    content = request.POST.get("content")

    q = Question(author=request.user, subject=subject, content=content)
    q.save()

    return HttpResponse("OK")

def home(request):
    return render(request, "home.html")

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
            return render(request, 'create_user.html', { 'form': form })
    form = RegistrationForm()
    return render(request, 'create_user.html', { 'form': form,
        'next': request.GET.get('next', '') })

def user_profile(request):
    return render(request, 'user_profile.html')

