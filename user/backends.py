from registration.backends.default import DefaultBackend
from user.forms import TwoStepRegForm

class RegBackend(DefaultBackend):
    def get_form_class(self, request):
        return TwoStepRegForm


