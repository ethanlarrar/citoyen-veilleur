from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
# Pensez a verifier que les validateurs fonctionnent avec les choices
# Afaire:
# finir model
# ré-écrire les pages du sites pour prendre en compte les nouveaux champs
class Website_alert(models.Model):
    creator = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                related_name="creator")
    title = models.CharField(max_length=200,
                             verbose_name=_("title"))
    url =  models.URLField(max_length=255, unique=True)
    remark = models.TextField(default="")
    deleted = models.BooleanField(default=False)
    date = models.DateTimeField(default=timezone.now)
    verify = models.BooleanField(default=False)
    site_closed = models.BooleanField(default=False)
    hour_video = models.PositiveIntegerField(default=0)
    minute_video = models.PositiveIntegerField(default=0)
    second_video = models.PositiveIntegerField(default=0)
    main_quotes = models.TextField(default="", blank=True)
    #liste de question sous forme de formulaire
    antisem_france = models.BooleanField(default=False)
    antisem_abroad = models.BooleanField(default=False)
    antisionisme_france = models.BooleanField(default=False)
    antisionisme_abroad = models.BooleanField(default=False)
    video = models.BooleanField(default=False)
    article = models.BooleanField(default=False)
    social_network = models.BooleanField(default=False)
    comments = models.BooleanField(default=False)
    regular_website = models.BooleanField(default=False)
    official_hater_website = models.BooleanField(default=False)
    legal_proceeding = models.BooleanField(default=False)
    only_alert = models.BooleanField(default=False)
    bad_user = models.BooleanField(default=False)
    extern_pseudo = models.CharField(max_length=200, default="", blank=True)
    # https://docs.djangoproject.com/fr/2.1/topics/db/models/, cf through
    voted_by = models.ManyToManyField(get_user_model(), through="Vote", related_name="website_alerts")
    
    def number_votes(self):
        return self.vote_set.all().count()

    def average_grade(self):
        k = 0
        number = 0
        for vote in self.vote_set.all():
            i = vote.grade
            k = k + i
            number += 1
        try: # Or possible to use if
            return k/number
        except ZeroDivisionError:
            return 0
    class Meta:
        permissions = (("can_verify", "Can verify a website alert"),)
            
    

class Vote(models.Model):
    user = models.ForeignKey(get_user_model(),
                             on_delete=models.CASCADE)
    website_alert = models.ForeignKey(Website_alert, on_delete=models.CASCADE)
    grade = models.IntegerField(default=1,                              
                                validators=[
                                    MaxValueValidator(5),
                                    MinValueValidator(0)
                                ])
    date = models.DateTimeField(default=timezone.now)    
    class Meta:
        unique_together = ('website_alert', 'user',)  
        
class ParamUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    points = models.IntegerField(default=0)
    ban = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    trust = models.BooleanField(default=False)
    intern_remark = models.TextField(default="")
    def red_list(self):
        ## Version 1
        # if self.points < -500:
        #     return True
        # else:
        #     return False
        return self.points < -500

  
        
