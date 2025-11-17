from django.contrib import admin
from .models import (
    # Modèles de la page d'accueil
    HeroFeature, 
    Statistique, 
    Client, 
    Temoignage, 
    FAQ,
    
    # Modèle de la page "À propos"
    PageAbout,
    
    # Modèle de la page "Services"
    Service,
    
    # Modèles du Portfolio
    CategorieProjet, 
    Projet, 
    ImageSliderProjet, 
    MetriqueProjet, 
    OutilTechnologie, 
    ImageProcessusProjet, 
    PointCleProjet,
    
    # Modèle de la page "Équipe"
    MembreEquipe
)

# --- Administration de la Page d'Accueil ---

@admin.register(HeroFeature)
class HeroFeatureAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre', 'icone')
    list_editable = ('ordre',)

@admin.register(Statistique)
class StatistiqueAdmin(admin.ModelAdmin):
    list_display = ('label', 'valeur', 'categorie', 'ordre')
    list_filter = ('categorie',)
    list_editable = ('ordre', 'categorie')

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ordre')
    list_editable = ('ordre',)

@admin.register(Temoignage)
class TemoignageAdmin(admin.ModelAdmin):
    list_display = ('nom', 'role', 'rating', 'ordre')
    list_editable = ('ordre', 'rating')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'ordre', 'est_active')
    list_editable = ('ordre', 'est_active')

# --- Administration de la Page "À Propos" ---

@admin.register(PageAbout)
class PageAboutAdmin(admin.ModelAdmin):
    
    # Empêche la création de plus d'une instance
    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)

    # Empêche la suppression de l'instance unique
    def has_delete_permission(self, request, obj=None):
        return False

# --- Administration de la Page "Services" ---

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'ordre', 'icone')
    list_editable = ('ordre',)

# --- Administration de la Page "Équipe" ---

@admin.register(MembreEquipe)
class MembreEquipeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'role', 'ordre')
    list_editable = ('ordre',)
    search_fields = ('nom', 'role')

# --- Administration du Portfolio (Projets) ---

# Classes "Inline" pour les ajouter à l'admin du modèle Projet
class ImageSliderProjetInline(admin.TabularInline):
    model = ImageSliderProjet
    extra = 1 # Affiche 1 champ vide par défaut
    ordering = ['ordre']

class MetriqueProjetInline(admin.TabularInline):
    model = MetriqueProjet
    extra = 1
    ordering = ['ordre']

class OutilTechnologieInline(admin.TabularInline):
    model = OutilTechnologie
    extra = 1
    ordering = ['ordre']

class ImageProcessusProjetInline(admin.TabularInline):
    model = ImageProcessusProjet
    extra = 1
    ordering = ['ordre']

class PointCleProjetInline(admin.TabularInline):
    model = PointCleProjet
    extra = 1
    ordering = ['ordre']


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ('titre', 'categorie', 'client', 'annee', 'date_publication')
    list_filter = ('categorie', 'annee', 'client')
    search_fields = ('titre', 'client', 'sous_titre')
    
    fieldsets = (
        (None, {
            'fields': ('titre', 'categorie', 'sous_titre', 'image_principale')
        }),
        ('Méta-données (Page Détail)', {
            'fields': ('client', 'duree', 'annee', 'services_utilises')
        }),
        ('Contenu (Page Détail)', {
            'fields': ('apercu_projet', 'le_defi', 'notre_approche', 'impact_resultats_texte', 'points_cles_description')
        }),
    )
    
    # Ajoute tous les modèles liés directement dans la page d'admin du projet
    inlines = [
        ImageSliderProjetInline,
        MetriqueProjetInline,
        OutilTechnologieInline,
        ImageProcessusProjetInline,
        PointCleProjetInline,
    ]

@admin.register(CategorieProjet)
class CategorieProjetAdmin(admin.ModelAdmin):
    list_display = ('nom',)