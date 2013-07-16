from django.shortcuts import get_object_or_404
from haystack.query import SearchQuerySet
from haystack.inputs import Exact
from haystack.views import basic_search

from entities.models import Entity

def place_search(request):
    place = request.GET.get('place')
    if place:
        searchqs = SearchQuerySet().filter(place=Exact(place))
        context = {'entity': get_object_or_404(Entity, slug=place),
                'base_template': 'place_base.html',
                }
        return basic_search(request, searchqueryset=searchqs,
                extra_context = context)
    return basic_search(request, extra_context={'base_template': 'base.html'})

