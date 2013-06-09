import re
from django import forms
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext as _
from user.models import Profile

unicode_username = forms.RegexField(label=_("Username"), max_length=30,
        regex=re.compile(r'^[\w.@+-]{4,}$', re.U),
        help_text = _("Required. 30 characters or fewer. Alphanumeric \
characters only (letters, digits and underscores)."),
        error_message = _("This value must contain only letters, \
numbers and underscores.")) 

class ProfileAdmin(admin.StackedInline):
    model = Profile

# Overrides django.contrib.auth.forms.UserCreationForm and changes 
# username to accept a wider range of character in the username. 
class UserCreationForm(UserCreationForm):
    username = unicode_username

# Overrides django.contrib.auth.forms.UserChangeForm and changes 
# username to accept a wider range of character in the username. 
class UserChangeForm(UserChangeForm): 
    username = unicode_username

class UnicodeUserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    inlines = (ProfileAdmin, )

admin.site.unregister(User)
admin.site.register(User, UnicodeUserAdmin)
