from django.contrib import admin

# Register your models here.
from .models import Website_alert, Vote, ParamUser

admin.site.register(Website_alert)
admin.site.register(Vote)
admin.site.register(ParamUser)
