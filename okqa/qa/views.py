import json
from django.http import HttpResponse, HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.utils.translation import ugettext as _
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from taggit.utils import parse_tags

from okqa.qa.models import Question, Answer, QuestionUpvote, CANDIDATES_GROUP_NAME
from okqa.qa.forms import AnswerForm, QuestionForm

from django.views.generic import DetailView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, BaseDetailView
from okqa.qa.mixins import JSONResponseMixin
from django.forms.models import model_to_dict


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


def candidate_detail(request, slug):
    candidate = get_object_or_404(User, username=slug)
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

    if request.user.is_authenticated() and \
       not request.user.upvotes.filter(question=question).exists():
        context["can_upvote"] = True
    else:
        context["can_upvote"] = False

    return render(request, "qa/question_detail.html", context)


class QuestionDetail(JSONResponseMixin, SingleObjectTemplateResponseMixin, BaseDetailView):
    model = Question
    template_name = 'qa/question_detail.html'
    context_object_name = 'question'
    slug_field = 'unislug'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetail, self).get_context_data(**kwargs)
        can_answer = self.object.can_answer(self.request.user)

        context['answers'] = self.object.answers.all()
        if can_answer:
            try:
                user_answer = self.object.answers.get(author=self.request.user)
                context['my_answer_form'] = AnswerForm(instance=user_answer)
                context['my_answer_id'] = user_answer.id
            except self.object.answers.model.DoesNotExist:
                context['my_answer_form'] = AnswerForm()
                context['can_answer'] = True

        if self.request.user.is_authenticated() and \
           not self.request.user.upvotes.filter(question=self.object).exists():
            context['can_upvote'] = True
        else:
            context['can_upvote'] = False

        return context

    def render_to_response(self, context):
            # Look for a 'format=json' GET argument
            if self.request.GET.get('format', 'html') == 'json' or self.request.is_ajax():
                data = {
                    'question': {
                        'subject': self.object.subject,
                        'content': self.object.content,
                        'author': self.object.author.username
                    }
                }

                return JSONResponseMixin.render_to_response(self, data)
            else:
                return SingleObjectTemplateResponseMixin.render_to_response(self, context)


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
        answer = Answer(author=request.user, question=question)

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
    return render_to_response("qa/post_question.html", {"form": form}, context_instance=RequestContext(request))


@login_required
def upvote_question(request, q_id):
    if request.method == "POST":
        q = get_object_or_404(Question, id=q_id)
        user = request.user

        if q.author == user or user.upvotes.filter(question=q):
            return HttpResponseForbidden(_("You already upvoted this question"))
        else:
            upvote = QuestionUpvote.objects.create(question=q, user=user)
            #TODO: use signals so the next line won't be necesary
            new_count = increase_rating(q)
            return HttpResponse(new_count)
    else:
        return HttpResponseForbidden(_("Use POST to upvote a question"))


@transaction.commit_on_success
def increase_rating(q):
    q = Question.objects.get(id=q.id)
    q.rating += 1
    q.save()
    return q.rating


def tagged_questions(request, tags):

    tags_list = tags.split(',')
    questions = Question.objects.filter(tags__name__in=tags_list)

    questions.order_by(ORDER_OPTIONS[request.GET.get('order', 'date')])

    return render(request, "qa/question_list.html", dict(questions=questions,
                                        current_tags=tags_list))


class RssQuestionFeed(Feed):
    """Simple feed to get all questions"""
    title = _('OK QA Question Feed')
    link = "/"
    description = _('Questions from OKQA')

    def items(self):
        return Question.objects.order_by('-updated_at')

    def item_title(self, item):
        return item.subject

    def item_description(self, item):
        return item.content


class AtomQuestionFeed(RssQuestionFeed):
    feed_type = Atom1Feed
    subtitle = RssQuestionFeed.description


class RssQuestionAnswerFeed(Feed):
    """"Give question, get all answers for that question"""

    def get_object(self, request, q_id):
        return get_object_or_404(Question, pk=q_id)

    def title(self, obj):
        return _('Answers for the question') + ' "%s' % obj.subject + '"'

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return _('A feed of all answers for the question') + ' "%s' % obj.subject + '"'

    def items(self, obj):
        return Answer.objects.filter(question=obj).order_by('-updated_at')


class AtomQuestionAnswerFeed(RssQuestionAnswerFeed):
    feed_type = Atom1Feed
    subtitle = RssQuestionAnswerFeed.description


class RssUserAnswerFeed(Feed):
    """"Give candidate, get all answers for that candidate"""

    def get_object(self, request, candidate_id):
        return get_object_or_404(User, pk=candidate_id)

    def title(self, obj):
        return _('Answers by') + '%s' % obj.get_full_name()

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return _('Get all answers by') + '%s' % obj.get_full_name()

    def items(self, obj):
        return Answer.objects.filter(author=obj).order_by('-updated_at')


class AtomUserAnswerFeed(RssUserAnswerFeed):
    feed_type = Atom1Feed
    subtitle = RssUserAnswerFeed.description
