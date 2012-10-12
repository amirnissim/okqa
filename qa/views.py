from django.shortcuts import render
from qa.models import Question
from django.http import HttpResponse, HttpResponseForbidden

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