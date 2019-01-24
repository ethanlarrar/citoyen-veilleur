from django.db import models
from django.utils import timezone

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Website_alert(models.Model):
    title = models.CharField(max_length=200)
    url =  models.URLField(max_length=255)
    remark = models.TextField()
    deleted = models.BooleanField()
    date = models.DateTimeField(default=timezone.now)
    verify = models.BooleanField()
    site_closed = models.BooleanField()
    class Meta:
        permissions = (("can_verify", "Can verify a website alert"),)
        
