from django.shortcuts import render,get_object_or_404,get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.urls import reverse
from .models import Website_alert, Vote  
from django.template import loader
from .forms import CreateForm, VoteForm
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required,permission_required
from django.core.paginator import Paginator
import base64
from django.utils.translation import gettext as _, ngettext

## TODO:
# 1) Pagination du alerts
# 2) plus tard: mettre plus de 3 alertes par page
# 3) créer une page présentation
# 4) faire la traduction
# 5) rendre formulaires beaux
# 6) sign in




# Cre=te your views here.
def index(request):
    # MÃ©thode 1
    # template = loader.get_template('sitereview/index.html')
    if request.user.is_authenticated:
        context = {'user': request.user}
    else:
        context = {'user': None}
    ## Pour y acceder en python: context['age_utilisateur']
    # return HttpResponse(template.render(context, request))
    ## MÃ©thode 2 (condensÃ©e)
    context.update({'remove_main_div': True})
    context.update({'tab':'home'})
    return render(request, 'sitereview/index.html', context)

def au_revoir(request):
    message = _("Good bye!")
    animal = _("Parrot")
    n_parrots = 4
    phrase = ngettext(
        'There is %(n_parrots)d parrot',
        'There are %(n_parrots)d parrots',
    n_parrots) % {
        'n_parrots': n_parrots,
    }
    return HttpResponse(message + animal + phrase)

def detail(request,question_id):
    ## Premier temps: utiliser des templates ici
    try:
        q = Question.objects.get(id=question_id)
        return HttpResponse(q.question_text)
    except Question.DoesNotExist:
        return HttpResponse("La question n'existe pas")

def afficher_questions(request):
    ### DeuxiÃ¨me temps:
    ## Afficher la liste de toutes les questions (seulement le titre)
    # Indice: cf tutoriel chapitre 2
    pass
    
### http://127.0.0.1:8000/sitereview/aurevoir

def display_website_alert(request,website_alert_id):
    ## get_list_or_404 pour une liste 
    website_alert = get_object_or_404(Website_alert,id=website_alert_id)
    if request.method == "POST":        
        form_vote = VoteForm(request.POST)
        if form_vote.is_valid():
            if request.user.is_anonymous:
                return HttpResponseRedirect(reverse('sitereview:already_voted'))
            elif  website_alert.voted_by.filter(username = request.user.username):
                vote = request.user.vote_set.get(website_alert = website_alert)
                vote.grade = form_vote.cleaned_data['grade']
                vote.save()
                return HttpResponseRedirect(reverse('sitereview:display_website_alert', args=(website_alert_id,)))
            else:
                new_vote = form_vote.save(commit=False)
                new_vote.user = request.user
                new_vote.website_alert = website_alert
                new_vote.save()
                return HttpResponseRedirect(reverse('sitereview:display_website_alert', args=(website_alert_id,)))
    else:
        form_vote = VoteForm()
    
    context = {"website_alert":website_alert, "form_vote":form_vote}    
    
    return render(request, 'sitereview/display_website_alert.html', context)

@login_required
@permission_required('sitereview.can_verify', raise_exception=True)
def list_website_alert(request, page=1):    
    sites = Website_alert.objects.all().order_by('-date')    
    p = Paginator(sites, 3)
    context = {"sites":p.page(page).object_list, "page":p.page(page)}
    context.update({'tab':'all_alerts'})
    return render(request, 'sitereview/list_website_alert.html/', context)

#def check_if_it_exists(request):
    


#MÃ©thode 2
@login_required
def create_website_alert(request):
    # MÃ©thode 1
    # if not request.user.is_authenticated:
    #     raise PermissionDenied
    if request.method == "POST":        
        # A form has been sent
        form = CreateForm(request.POST)
        form_vote = VoteForm(request.POST)
        if form.is_valid() and form_vote.is_valid():
            new_website = form.save(commit=False)
            new_website.creator = request.user
            new_website.save()
            new_vote = form_vote.save(commit=False)
            new_vote.user = request.user
            new_vote.website_alert = new_website
            new_vote.save()
            # new_website.save_m2m()
            return HttpResponseRedirect(reverse('sitereview:display_website_alert', args=(new_website.id,)))
    else:
        # The user wants to see the form
        form = CreateForm()
        form_vote = VoteForm()
    context = {'form': form,'form_vote': form_vote }
    context.update({'tab':'create_alerts'})
    return render(request, 'sitereview/create_website_alert.html', context)

@login_required
@permission_required('sitereview.can_verify', raise_exception=True)
def validate_list_website_alert(request, page=1):
    sites = Website_alert.objects.filter(verify = False)
    p = Paginator(sites, 3)
    context = {'user': request.user, "sites":p.page(page).object_list, "page":p.page(page)}
    context.update({'tab':'validate_list'})
    return render(request, 'sitereview/validate_list_website_alert.html', context)

def list_verified_website_alert(request):
    sites = Website_alert.objects.filter(verify = True).order_by('-date')
    context = {"sites":sites}
    context.update({'tab':'list_verified_website_alert'})
    return render(request, 'sitereview/list_verified_website_alert.html', context)

def website_exists(request, url_b64):
    print(url_b64)
    try:
        url = base64.b64decode(url_b64).decode("utf-8")
    except:
        url = ""
    print(url)
    sites = Website_alert.objects.filter(url = url) # le premier url se rÃ©fÃ¨re au nom du champ (colonne) dans la base de donnÃ©e, le deuxiÃ¨me url se rÃ©fÃ¨re Ã  la variable dÃ©finie juste avant
    if sites: # Sert Ã  vÃ©rifier si 'sites' n'est pas vide, comme if len(sites) > 0
        return JsonResponse({'exists': True, 'url': url})
    else:
        return JsonResponse({'exists': False, 'url': url})

@login_required
@permission_required('sitereview.can_verify', raise_exception=True)
def validate_website_alert(request, website_alert_id):

    website_alert = get_object_or_404(Website_alert,id=website_alert_id)
    website_alert.verify = True
    website_alert.save()
    return HttpResponseRedirect(reverse('sitereview:display_website_alert', args=(website_alert_id,)))

@login_required
@permission_required('sitereview.can_unverify', raise_exception=True)
def unvalidate_website_alert(request, website_alert_id):
    website_alert = get_object_or_404(Website_alert,id=website_alert_id)
    website_alert.verify = False
    website_alert.save()
    return HttpResponseRedirect(reverse('sitereview:display_website_alert', args=(website_alert_id,)))

@login_required
@permission_required('sitereview.can_verify', raise_exception=True)
def edit_website_alert(request, website_alert_id):
    website_alert = get_object_or_404(Website_alert,id=website_alert_id)
    if request.method == "POST":        
        # A form has been sent
        form = CreateForm(request.POST, instance=website_alert)
        if form.is_valid():
            new_website = form.save(commit=False)            
            new_website.save()
            return HttpResponseRedirect(reverse('sitereview:display_website_alert', args=(new_website.id,)))
    else:
        # The user wants to see the form
        form = CreateForm(instance=website_alert)
    context = {'form': form, 'website_alert':website_alert }
    context.update({'tab':'edit_alerts'})
    return render(request, 'sitereview/edit_website_alert.html', context)
    
    
    


