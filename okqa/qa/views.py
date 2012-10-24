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
from okqa.qa.forms import AnswerForm, QuestionForm

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
    tags = Question.tags.all().annotate(count=Count("question"))

    return render_to_response("qa/question_list.html", dict(questions=questions, tags=tags),
                              context_instance=RequestContext(request))

def view_question(request, q_id):
    # import pdb; pdb.set_trace()
    question = get_object_or_404(Question, id=q_id)
    can_answer = question.can_answer(request.user)
    context = RequestContext(request, {"question": question,
        "answers": question.answers.all(),
        })
    if can_answer:
        try:
            user_answer = question.answers.get(author=request.user)
            context["my_answer_form"] = AnswerForm(instance=user_answer)
            context["my_answer_id"] = user_answer.id
        except question.answers.model.DoesNotExist:
            context["my_answer_form"] = AnswerForm()
            context["can_answer"] = True

    return render_to_response("qa/question_detail.html", context)

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
def post_answer(request, q_id):
    context = {}
    question = Question.objects.get(id=q_id)

    if not question.can_answer(request.user):
        return HttpResponseForbidden(_("You must be logged in as a candidate to post answers"))

    try:
        # make sure the user haven't answered already
        answer = question.answers.get(author=request.user)
    except question.answers.model.DoesNotExist:
        answer = Answer(author=request.user, question = question)

    answer.content = request.POST.get("content")

    answer.save()
    return HttpResponseRedirect(question.get_absolute_url())

@login_required
def post_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()
            return HttpResponseRedirect(question.get_absolute_url())

        #TODO: make this better - show the form
        # return HttpResponseRedirect("/#question_modal")
    elif request.method == "GET":
        form = QuestionForm()
    return render_to_response("qa/post_question.html", {"form": form }, context_instance=RequestContext(request))

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
