# Django imports
from django import forms
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext as _
from django.template.context import RequestContext
# pluggable apps
from haystack.query import SearchQuerySet
from haystack.inputs import Exact
from haystack.views import basic_search
from entities.models import Entity
from chosen import forms as chosenforms
# our apps
from qa.models import Question

class EntityForm(forms.Form):
    ''' this form is used only to display the field, input
        is handled by the client
    '''
    entity = chosenforms.ChosenModelChoiceField(
                queryset=Entity.objects.filter(division__index=3),
                label=_('Move to'), required=False)

def place_search(request):
    ''' A view to search in a specific place '''
    place = request.GET.get('place')
    if place:
        searchqs = SearchQuerySet().filter(place=Exact(place))
        context = {'entity': get_object_or_404(Entity, slug=place),
                'base_template': 'place_base.html',
                }
        return basic_search(request, searchqueryset=searchqs,
                extra_context = context)
    return basic_search(request, extra_context={'base_template': 'base.html'})

def home(request):
    ''' home sweet home! '''
    #TODO: add answers and candidates object lists
    context = RequestContext(request, {
        "form": EntityForm(),
        "questions": Question.objects.all().order_by('-created_at'),
        "by_date": True,
        })
    return render(request, "home.html", context)

