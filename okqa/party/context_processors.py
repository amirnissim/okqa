from django.contrib.auth.forms import AuthenticationForm
from haystack.forms import SearchForm

def forms(request):
    context = {"search_form": SearchForm()}
    if not request.user.is_authenticated():
        context["login_form"] = AuthenticationForm()
    return context


