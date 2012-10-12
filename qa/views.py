from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.context import RequestContext
from qa.models import Question, Answer
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest

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

def list_questions(request):
    questions = Question.objects.all()
    return render_to_response("questions.html", locals(), context_instance=RequestContext(request))

def view_question(request, q_id):
    question = get_object_or_404(Question, id=q_id)
    answers = question.answers.all()
    return render_to_response("question.html", locals(), context_instance=RequestContext(request))

def add_answer(request, q_id):
    if not request.user.is_authenticated(): # TODO: check that user is a candidate (can answer questions)
        return HttpResponseForbidden()

    question = Question.objects.get(id=q_id)
    content = request.POST.get("content")

    if not (question and content):
        return HttpResponseBadRequest()

    answer = Answer(author=request.user, content=content, question=question)
    answer.save()

    return HttpResponse("Your answer was recorded")