from django.contrib import admin

# Register your models here.
from .models import Question, Choice, Website_alert

admin.site.register(Website_alert)
admin.site.register(Question)
