from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question,Website_alert   
from django.template import loader
from .forms import CreateForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

## TODO:
# 1) afficher seulement les sites validés
# 2) afficher via un système de pagination
# 3) créer une page qui valide un site
# 4) ajouter une verification pour seuls les personnes dans le groupe validateurs puisse valider le site https://docs.djangoproject.com/fr/2.1/topics/auth/default/.
# 5) Afficher les boutons pour changer de page.


# Cre=te your views here.
def index(request):
    # Méthode 1
    # template = loader.get_template('sitereview/index.html')
    if request.user.is_authenticated:
        context = {'user': request.user}
    else:
        context = {'user': None}
    ## Pour y acceder en python: context['age_utilisateur']
    # return HttpResponse(template.render(context, request))
    ## Méthode 2 (condensée)
    context.update({'tab':'home'})
    return render(request, 'sitereview/index.html', context)

def au_revoir(request):
    return HttpResponse("Au revoir!")

def detail(request,question_id):
    ## Premier temps: utiliser des templates ici
    try:
        q = Question.objects.get(id=question_id)
        return HttpResponse(q.question_text)
    except Question.DoesNotExist:
        return HttpResponse("La question n'existe pas")

def afficher_questions(request):
    ### Deuxième temps:
    ## Afficher la liste de toutes les questions (seulement le titre)
    # Indice: cf tutoriel chapitre 2
    pass
    
### http://127.0.0.1:8000/sitereview/aurevoir

def display_website_alert(request,website_alert_id):
    ## get_list_or_404 pour une liste 
    website_alert = get_object_or_404(Website_alert,id=website_alert_id)
    context = {"website_alert":website_alert}
    return render(request, 'sitereview/display_website_alert.html', context)     

def list_website_alert(request, page=1):    
    sites = Website_alert.objects.all()
    p = Paginator(sites, 3)
    context = {"sites":p.page(page).object_list, "page":p.page(page)}
    context.update({'tab':'all_alerts'})
    return render(request, 'sitereview/list_website_alert.html/', context) 

#Méthode 2
@login_required
def create_website_alert(request):
    # Méthode 1
    # if not request.user.is_authenticated:
    #     raise PermissionDenied
    if request.method == "POST":        
        # A form has been sent
        form = CreateForm(request.POST)
        if form.is_valid():
            new_website = form.save(commit=False)
            new_website.deleted = False
            new_website.verify = False
            new_website.site_closed = False
            new_website.save()
            # new_website.save_m2m()
            return HttpResponseRedirect(reverse('sitereview:display_website_alert', args=(new_website.id,)))
    else:
        # The user wants to see the form
        form = CreateForm()
    context = {'form': form }
    context.update({'tab':'create_alerts'})
    return render(request, 'sitereview/create_website_alert.html', context)

def validate_list_website_alert(request):
    sites = Website_alert.objects.filter(verify = False)
    context = {"sites":sites}
    context.update({'tab':'validate_list'})
    return render(request, 'sitereview/validate_list_website_alert.html', context)

def list_verified_website_alert(request):
    sites = Website_alert.objects.filter(verify = True)
    context = {"sites":sites}
    context.update({'tab':'list_verified_website_alert'})
    return render(request, 'sitereview/list_verified_website_alert.html', context)
