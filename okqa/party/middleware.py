from django.contrib.auth.forms import AuthenticationForm

class PartyMiddleware:
    def process_request(self, request):
        if not request.user.is_authenticated():
            request.login_form = AuthenticationForm
        return None

