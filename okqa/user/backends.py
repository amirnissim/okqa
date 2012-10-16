from registration.backends.default import DefaultBackend
from registration import signals
from user.forms import TwoStepRegForm

class RegBackend(DefaultBackend):
    def get_form_class(self, request):
        return TwoStepRegForm

    def register(self, request, **kwargs):
        user = super(RegBackend, self).register(request, **kwargs)
        user.first_name = kwargs['first_name']
        user.last_name = kwargs['last_name']
        user.save()
        return user




