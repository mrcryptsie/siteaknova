from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from core.storage_backends import SupabaseStorage  # <-- import SupabaseStorage

# ===============================================
# MODÈLES POUR LA PAGE D'ACCUEIL (index.html)
# ===============================================

class HeroFeature(models.Model):
    # --- MODIFICATION START : Changement de CharField à ImageField ---
    icone = models.ImageField(
        upload_to='hero_features/', 
        storage=SupabaseStorage(), 
        verbose_name="Icône / Image",
        help_text="Upload une image (PNG, SVG, JPG) qui sera affichée en blanc sur fond vert."
    )
    # --- MODIFICATION END ---
    
    titre = models.CharField(max_length=100)
    description = models.TextField()
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Feature (Accueil)"
        verbose_name_plural = "Features (Accueil)"

    def __str__(self):
        return self.titre

class Statistique(models.Model):
    CATEGORIES = [
        ('hero', 'Carte Flottante Hero'),
        ('stats', 'Section Chiffres Clés'),
    ]
    categorie = models.CharField(max_length=10, choices=CATEGORIES, default='stats')
    valeur = models.CharField(max_length=20, help_text="La valeur (ex: '2025' ou '7+')")
    label = models.CharField(max_length=100, help_text="Le titre (ex: 'Année de création')")
    description = models.TextField(blank=True, null=True, help_text="Courte description (pour la section Stats)")
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Statistique"
        verbose_name_plural = "Statistiques"

    def __str__(self):
        return f"{self.label}: {self.valeur}"

class Client(models.Model):
    nom = models.CharField(max_length=100)
    logo = models.ImageField(
        upload_to='client_logos/',
        storage=SupabaseStorage(),  # <-- Forcer Supabase
        help_text="Logo du client (sera affiché en grayscale)"
    )
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.nom

class Temoignage(models.Model):
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="Ex: 'Responsable Environnement, Entreprise Agro'")
    texte = models.TextField(help_text="Le contenu du témoignage")
    image = models.ImageField(
        upload_to='testimonial_photos/',
        storage=SupabaseStorage()  # <-- Forcer Supabase
    )
    rating = models.PositiveIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Note de 1 à 5"
    )
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Témoignage"
        verbose_name_plural = "Témoignages"

    def __str__(self):
        return self.nom

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    reponse = models.TextField()
    est_active = models.BooleanField(default=False, help_text="Cochez pour que cette question soit ouverte par défaut (une seule recommandée)")
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Question (FAQ)"
        verbose_name_plural = "Questions (FAQ)"

    def __str__(self):
        return self.question

# ===============================================
# MODÈLE POUR LA PAGE "À PROPOS" (about.html)
# ===============================================

class PageAbout(models.Model):
    mission_titre = models.CharField(max_length=200, default="Notre mission")
    mission_texte = models.TextField(blank=True, help_text="Le paragraphe principal sous 'Notre mission'")
    vision_titre = models.CharField(max_length=200, default="Notre vision")
    vision_texte = models.TextField(blank=True)
    equipe_titre = models.CharField(max_length=200, default="Notre équipe")
    equipe_texte = models.TextField(blank=True)
    
    image = models.ImageField(
        upload_to='about_page/',
        storage=SupabaseStorage(),  # <-- Forcer Supabase
        blank=True, null=True,
        help_text="L'image principale de la page À Propos"
    )
    image_overlay_titre = models.CharField(max_length=100, default="Professionnalisme & Rigueur")
    image_overlay_texte = models.CharField(max_length=200, default="Des solutions durables et performantes")

    class Meta:
        verbose_name = "Page À Propos"
        verbose_name_plural = "Page À Propos"

    def __str__(self):
        return "Contenu de la page À Propos"

# ===============================================
# MODÈLE POUR LA PAGE "SERVICES" (services.html)
# ===============================================

class Service(models.Model):
    icone = models.CharField(max_length=50, help_text="Nom de l'icône Bootstrap (ex: 'bi bi-tree')")
    titre = models.CharField(max_length=200)
    description = models.TextField(help_text="Courte description du service.")
    ordre = models.PositiveIntegerField(default=0, help_text="Pour trier l'affichage (le plus petit en premier).")

    class Meta:
        ordering = ['ordre']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.titre

# ===============================================
# MODÈLES POUR LE PORTFOLIO
# ===============================================

class CategorieProjet(models.Model):
    nom = models.CharField(max_length=100, unique=True, help_text="Ex: Étude d'Impact, Analyses")

    class Meta:
        verbose_name = "Catégorie de Projet"
        verbose_name_plural = "Catégories de Projet"
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Projet(models.Model):
    titre = models.CharField(max_length=255)
    categorie = models.ForeignKey(CategorieProjet, on_delete=models.SET_NULL, null=True, blank=True)
    sous_titre = models.TextField(help_text="La description courte sous le titre (sur la page détail)")
    image_principale = models.ImageField(
        upload_to='projets/miniatures/',
        storage=SupabaseStorage(),  # <-- Forcer Supabase
        help_text="Image affichée sur la page de liste (galerie)"
    )
    
    client = models.CharField(max_length=200, blank=True)
    duree = models.CharField(max_length=100, blank=True, help_text="Ex: '6 mois'")
    annee = models.PositiveIntegerField(default=2025)
    services_utilises = models.CharField(max_length=200, blank=True, help_text="Ex: 'Étude d'Impact, Analyses, Conseil'")
    
    apercu_projet = models.TextField(blank=True, help_text="Le texte dans 'Aperçu du Projet'")
    le_defi = models.TextField(blank=True, help_text="Le texte dans 'Le Défi'")
    notre_approche = models.TextField(blank=True, help_text="Le texte dans 'Notre Approche'")
    impact_resultats_texte = models.TextField(blank=True, help_text="Le petit paragraphe 'Impact & Results'")
    points_cles_description = models.TextField(blank=True, help_text="La description sous 'Points Clés du Projet'")
    date_publication = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-annee', '-date_publication']
        verbose_name = "Projet"
        verbose_name_plural = "Projets"

    def __str__(self):
        return self.titre
    
    def get_absolute_url(self):
        return reverse('portfolio_detail', kwargs={'pk': self.pk})

# --- Modèles "Inline" liés au Projet ---

class ImageSliderProjet(models.Model):
    projet = models.ForeignKey(Projet, related_name='images_slider', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='projets/slider/',
        storage=SupabaseStorage()  # <-- Forcer Supabase
    )
    legende = models.CharField(max_length=200, blank=True)
    ordre = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
        verbose_name = "Image du Slider"

class MetriqueProjet(models.Model):
    projet = models.ForeignKey(Projet, related_name='metriques', on_delete=models.CASCADE)
    valeur = models.CharField(max_length=50, help_text="Ex: '85%' ou '500+'")
    label = models.CharField(max_length=100, help_text="Ex: 'Réduction des impacts'")
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Métrique"

class OutilTechnologie(models.Model):
    projet = models.ForeignKey(Projet, related_name='outils', on_delete=models.CASCADE)
    categorie = models.CharField(max_length=100, help_text="Ex: 'Analyses & Mesures', 'Modélisation'")
    nom = models.CharField(max_length=100, help_text="Ex: 'Chromatographie', 'SIG'")
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['categorie', 'ordre']
        verbose_name = "Outil/Technologie"

class ImageProcessusProjet(models.Model):
    projet = models.ForeignKey(Projet, related_name='images_processus', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to='projets/processus/',
        storage=SupabaseStorage()  # <-- Forcer Supabase
    )
    legende = models.CharField(max_length=200)
    est_large = models.BooleanField(default=False, help_text="Cochez si cette image doit être plus grande (style 'large')")
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Image de Processus"

class PointCleProjet(models.Model):
    projet = models.ForeignKey(Projet, related_name='points_cles', on_delete=models.CASCADE)
    icone = models.CharField(max_length=50, default="bi bi-clipboard-data", help_text="Nom de l'icône Bootstrap")
    titre = models.CharField(max_length=200)
    description = models.TextField()
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Point Clé"

# ===============================================
# MODÈLE POUR LA PAGE "ÉQUIPE" (team.html)
# ===============================================

class MembreEquipe(models.Model):
    nom = models.CharField(max_length=200)
    role = models.CharField(max_length=200, help_text="Ex: 'Directeur Scientifique'")
    description = models.TextField(help_text="Courte biographie du membre.")
    image = models.ImageField(
        upload_to='equipe/',
        storage=SupabaseStorage(),  # <-- Forcer Supabase
        help_text="Photo du membre (de préférence carrée ou ratio 1/1.1)"
    )
    ordre = models.PositiveIntegerField(default=0, help_text="Pour trier l'affichage (le plus petit en premier).")

    lien_twitter = models.URLField(blank=True, help_text="Lien complet (URL) vers le profil Twitter/X")
    lien_linkedin = models.URLField(blank=True, help_text="Lien complet (URL) vers le profil LinkedIn")
    email = models.EmailField(blank=True, help_text="Adresse email publique (optionnel)")

    class Meta:
        ordering = ['ordre']
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"

    def __str__(self):
        return self.nom