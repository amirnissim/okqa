from django.contrib.auth.forms import AuthenticationForm


def forms(request):
        if not request.user.is_authenticated():
            return {"login_form": AuthenticationForm}
        else:
            return {}


