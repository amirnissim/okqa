from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _

from models import *

class ProfileForm(forms.Form):
    username = forms.RegexField(label=_("username"), max_length=30, regex=r'^(?u)[\w.@+-]{4,}$',
                                help_text= _('Please use 4 letters or more'))
    first_name = forms.CharField(label=_('first name'), max_length = 15)
    last_name = forms.CharField(label=_('last name'), max_length = 20)
    email = forms.EmailField(required=False ,label=_(u'email address'))
    url = forms.URLField(required=False ,label=_(u'home page'))
    bio = forms.CharField(label=_('bio'),
                          widget=forms.Textarea(attrs={'rows':5}))
    email_notification = forms.ChoiceField(choices = NOTIFICATION_PERIOD_CHOICES,
                                           label = _('E-Mail Notifications'),
                                           help_text = _('Should we send you e-mail notification about updates to things you follow on the site?'))

    def __init__(self, user = None, *args, **kw):
        super(ProfileForm, self).__init__(*args, **kw)
        self.user = user
        self.profile = user.profile
        if self.user:
            self.initial = {'username': self.user.username,
                            'email': self.user.email,
                            'first_name': self.user.first_name,
                            'last_name': self.user.last_name,
                            'bio': self.profile.bio,
                            'email_notification': self.profile.email_notification,
                            'url': self.profile.url,
                           }

    def clean_username(self):
        data = self.cleaned_data['username']
        if data ==  self.user.username:
            return data
        try:
            User.objects.get(username = data)
            raise forms.ValidationError("This username is already taken.")
        except User.DoesNotExist:
            return data

    def save(self, commit = True):
        user = self.user
        if self.cleaned_data['email'] != None:
            if user.email != self.cleaned_data['email']: #email changed - user loses comment permissions, until he validates email again.
                #TODO: send validation email
                pass
            user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        self.profile.bio = self.cleaned_data['bio']
        self.profile.email_notification = self.cleaned_data['email_notification']
        self.profile.url = self.cleaned_data['url']

        if commit:
            user.save()
            self.profile.save()
        return user

invitation_default_text, create = FlatPage.objects.get_or_create(url='/_invite_candidate/',
        defaults={'title': _('the voters are waiting for your answers'),
                  'content': _("The Q&A site is happy to invite you to answer\
 voters' questions. please click {{activation_url}} to activate your account"),
                 })

class AddCandidateForm(forms.Form):
    username = forms.RegexField(label=_("username"), max_length=30, regex=r'^(?u)[\w.@+-]{4,}$',
                                help_text= _('Please use 4 letters or more'))
    first_name = forms.CharField(label=_('first name'), max_length = 15)
    last_name = forms.CharField(label=_('last name'), max_length = 20)
    invitation_subject = forms.CharField(label=_('email subject'), max_length = 60,
            initial=invitation_default_text.title)
    invitation_body = forms.CharField(label=_('email body'), widget = forms.Textarea,
            initial = invitation_default_text.content)
    email = forms.EmailField(required=False ,label=_(u'email address'))

    def clean_username(self):
        data = self.cleaned_data['username']
        try:
            User.objects.get(username = data)
            raise forms.ValidationError("This username is already taken.")
        except User.DoesNotExist:
            return data

class ActivateCandidateForm(SetPasswordForm):
    url = forms.URLField(required=False ,label=_(u'home page'))
    bio = forms.CharField(label=_('bio'),
                          widget=forms.Textarea(attrs={'rows':5}))

    def save(self, commit=True):
        super(ActivateCandidateForm, self).save(commit)
        profile = self.user.profile
        profile.url = self.cleaned_data['url']
        profile.bio = self.cleaned_data['bio']
        if commit:
            profile.save()
        return self.user
