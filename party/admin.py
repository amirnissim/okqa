from django.contrib import admin
from .models import *

class PartyAdmin(admin.ModelAdmin):
    pass

admin.site.register(Party, PartyAdmin)
