from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.conf import settings # Importez settings
from django.core.mail import send_mail # Importez send_mail

# Import de tous les modèles nécessaires
from .models import (
    HeroFeature, 
    Statistique, 
    Client, 
    Temoignage, 
    FAQ,
    PageAbout,
    Service,
    CategorieProjet, 
    Projet,
    MembreEquipe
)

# Import de tous les formulaires
from .forms import ContactForm, NewsletterForm

# ===============================================
# VUES DES PAGES PRINCIPALES
# ===============================================

def index(request):
    hero_features = HeroFeature.objects.all()
    hero_stats = Statistique.objects.filter(categorie='hero')
    stats_cles = Statistique.objects.filter(categorie='stats')
    clients = Client.objects.all()
    temoignages = Temoignage.objects.all()
    faqs = FAQ.objects.all()
    contact_form = ContactForm()
    context = {
        'hero_features': hero_features,
        'hero_stats': hero_stats,
        'stats_cles': stats_cles,
        'clients': clients,
        'temoignages': temoignages,
        'faqs': faqs,
        'contact_form': contact_form,
    }
    return render(request, 'index.html', context)

def about(request):
    page_about, created = PageAbout.objects.get_or_create(id=1)
    clients = Client.objects.all()
    temoignages = Temoignage.objects.all()
    context = {
        'page_about': page_about,
        'clients': clients,
        'temoignages': temoignages,
    }
    return render(request, 'about.html', context)

def services(request):
    services_list = Service.objects.all()
    context = {
        'services_list': services_list,
    }
    return render(request, 'services.html', context)

def team(request):
    membres_equipe = MembreEquipe.objects.all()
    context = {
        'membres_equipe': membres_equipe,
    }
    return render(request, 'team.html', context)

# ===============================================
# VUE CONTACT (MISE À JOUR)
# ===============================================

def contact(request):
    success = False

    if request.method == 'POST':
        form = ContactForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            
            # Préparation de l'email
            sujet = f"Nouveau message de contact: {cd['subject']}"
            message_body = f"""
            Vous avez reçu un nouveau message depuis le site web Aknova.
            
            Nom: {cd['name']}
            Email: {cd['email']}
            Téléphone: {cd.get('phone', 'Non fourni')}
            
            Message:
            {cd['message']}
            """
            
            try:
                # Envoi de l'email
                send_mail(
                    sujet,
                    message_body,
                    settings.DEFAULT_FROM_EMAIL, # L'email de l'expéditeur (votre gmail)
                    ['n86073523@gmail.com'],       # LISTE des destinataires (l'email de l'entreprise)
                    fail_silently=False,
                )
                success = True
                form = ContactForm() # Réinitialiser le formulaire
                
            except Exception as e:
                # Gérer l'échec de l'envoi (ex: mauvais mot de passe)
                # Vous verrez cette erreur dans votre console runserver
                print(f"Erreur lors de l'envoi de l'email: {e}")
                # Vous pouvez ajouter une erreur au formulaire ici si vous le souhaitez
                # form.add_error(None, "Erreur lors de l'envoi du message. Veuillez réessayer.")
                pass

    else:
        form = ContactForm()

    context = {
        'contact_form': form,
        'success': success,
    }
    return render(request, 'contact.html', context)

# ===============================================
# VUES DU PORTFOLIO
# ===============================================

def portfolio_list(request):
    projets = Projet.objects.all()
    categories = CategorieProjet.objects.all()
    context = {
        'projets': projets,
        'categories': categories,
    }
    return render(request, 'portfolio_list.html', context) 

def portfolio_detail(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    next_project = Projet.objects.filter(date_publication__gt=projet.date_publication).order_by('date_publication').first()
    prev_project = Projet.objects.filter(date_publication__lt=projet.date_publication).order_by('-date_publication').first()
    context = {
        'projet': projet,
        'next_project': next_project,
        'prev_project': prev_project,
    }
    return render(request, 'portfolio_detail.html', context)

# ===============================================
# VUES DES FORMULAIRES (POST uniquement)
# ===============================================

def newsletter_signup(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            # TODO: Logique pour enregistrer l'email
            pass
        return redirect(request.META.get('HTTP_REFERER', 'index'))
    
    return HttpResponseNotAllowed(['POST'])