from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

from taggit.utils import parse_tags

from okqa.qa.models import Question, Answer, QuestionUpvote, CANDIDATES_GROUP_NAME

# the order options for the list views
ORDER_OPTIONS = {'date': '-created_at', 'rating': '-rating'}

def home(request):
    return render(request, "home.html")

def candidates(request):
    """
    list candidates ordered by number of answers
    """
    g = Group.objects.get(name=CANDIDATES_GROUP_NAME)
    candidates = g.user_set.all().annotate(num_answers=Count('answers')).order_by("-num_answers")
    return render_to_response("candidates.html", locals(), context_instance=RequestContext(request))

def view_candidate(request, candidate_id):
    candidate = get_object_or_404(User, id=candidate_id)
    answers = candidate.answers.all()
    return render_to_response("view_candidate.html", locals(), context_instance=RequestContext(request))

def members(request):
    g = Group.objects.get(name="members")
    members = g.user_set.all()
    return render_to_response("members.html", locals(), context_instance=RequestContext(request))

def view_member(request, voter_id):
    member = get_object_or_404(User, id=member_id)
    return render_to_response("view_member.html", locals(), context_instance=RequestContext(request))

def questions(request):
    """
    list questions ordered by number of upvotes
    """
    
    try:
        order = ORDER_OPTIONS[request.GET.get('order', None)]
    except KeyError:
        order = '-created_at'

    questions = Question.objects.all().order_by(order)
    #TODO: optimize
    tags = Question.tags.all()
    for t in tags:
        t.count = Question.objects.filter(tags=t).count()

    return render_to_response("questions.html", locals(), context_instance=RequestContext(request))

def view_question(request, q_id):
    # TODO: add answer edit forum
    # context ["my_answer_form"] = AnswerEditForm.form(current_answer)
    # context ["my_answer_id"] = current_answer.id
    question = get_object_or_404(Question, id=q_id)
    answers = question.answers.all()
    can_answer = question.can_answer(request.user)
    return render_to_response("view_question.html", locals(), context_instance=RequestContext(request))

def add_question(request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden(_("You cannot post questions"))

    subject = request.POST.get("subject")
    content = request.POST.get("content")

    q = Question(author=request.user, subject=subject, content=content)
    q.save()

    tags = parse_tags(request.POST.get("tags", []))
    for tag in tags:
        q.tags.add(tag)

    return HttpResponse("OK")

def home(request):
    return render(request, "home.html")

@login_required
def add_answer(request, q_id):
    context = {}
    question = Question.objects.get(id=q_id)

    if not question.can_answer(request.user):
        return HttpResponseForbidden(_("You must be logged in as a candidate to post answers"))

    try:
        current_answer = question.answers.get(author=request.user)
    except question.answers.model.MultipleObjectsReturned:
        current_answer = True

    if current_answer:
        messages.info(request, 
                _("You have already answered the question. To change your answer, hover over it and click the pen icon."))

    content = request.POST.get("content")

    if not (question and content):
        return HttpResponseBadRequest(_("Question does not exist, or empty answer"))

    question.answers.create(author=request.user, content=content)
    return HttpResponseRedirect(question.get_absolute_url())

def upvote_question(request, q_id):
    q = get_object_or_404(Question, id=q_id)
    user = request.user

    if q.author == user:
        return HttpResponseForbidden(_("You cannot upvote your own question"))
    voted_questions = [vote.question for vote in user.upvotes.all()]
    if q in voted_questions:
        return HttpResponseForbidden(_("You already upvoted this question"))
    else:
        upvote = QuestionUpvote(question=q, user=user)
        upvote.save()
        increase_rating(q)
    return HttpResponse(_("Your vote was recorded"))

@transaction.commit_on_success
def increase_rating(q):
    q = Question.objects.get(id=q.id)
    q.rating += 1
    q.save()
