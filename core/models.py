from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

# ===============================================
# MODÈLES POUR LA PAGE D'ACCUEIL (index.html)
# ===============================================

class HeroFeature(models.Model):
    """ Modèle pour les 4 "Features" (cartes) sous le Hero """
    icone = models.CharField(max_length=50, help_text="Nom de l'icône Bootstrap (ex: 'bi bi-flask')")
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
    """ Modèle pour les Chiffres Clés (Stats) """
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
    """ Modèle pour les logos des Clients """
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='client_logos/', help_text="Logo du client (sera affiché en grayscale)")
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.nom

class Temoignage(models.Model):
    """ Modèle pour les Témoignages """
    nom = models.CharField(max_length=100)
    role = models.CharField(max_length=100, help_text="Ex: 'Responsable Environnement, Entreprise Agro'")
    texte = models.TextField(help_text="Le contenu du témoignage")
    image = models.ImageField(upload_to='testimonial_photos/')
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
    """ Modèle pour la section FAQ """
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
    """ Modèle Singleton pour gérer le contenu de la page À Propos """
    # Section principale
    mission_titre = models.CharField(max_length=200, default="Notre mission")
    mission_texte = models.TextField(blank=True, help_text="Le paragraphe principal sous 'Notre mission'")
    vision_titre = models.CharField(max_length=200, default="Notre vision")
    vision_texte = models.TextField(blank=True)
    equipe_titre = models.CharField(max_length=200, default="Notre équipe")
    equipe_texte = models.TextField(blank=True)
    
    # Image et son overlay
    image = models.ImageField(upload_to='about_page/', blank=True, null=True, help_text="L'image principale de la page À Propos")
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
    """ Modèle pour les Services (affichés en grille) """
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
# MODÈLES POUR LE PORTFOLIO (portfolio_list.html & portfolio_detail.html)
# ===============================================

class CategorieProjet(models.Model):
    """ Catégories pour filtrer les projets (ex: Étude d'Impact) """
    nom = models.CharField(max_length=100, unique=True, help_text="Ex: Étude d'Impact, Analyses")

    class Meta:
        verbose_name = "Catégorie de Projet"
        verbose_name_plural = "Catégories de Projet"
        ordering = ['nom']

    def __str__(self):
        return self.nom

class Projet(models.Model):
    """ Modèle principal pour un projet/réalisation """
    titre = models.CharField(max_length=255)
    categorie = models.ForeignKey(CategorieProjet, on_delete=models.SET_NULL, null=True, blank=True)
    sous_titre = models.TextField(help_text="La description courte sous le titre (sur la page détail)")
    image_principale = models.ImageField(upload_to='projets/miniatures/', help_text="Image affichée sur la page de liste (galerie)")
    
    # Meta-données (Page Détail)
    client = models.CharField(max_length=200, blank=True)
    duree = models.CharField(max_length=100, blank=True, help_text="Ex: '6 mois'")
    annee = models.PositiveIntegerField(default=2025)
    services_utilises = models.CharField(max_length=200, blank=True, help_text="Ex: 'Étude d'Impact, Analyses, Conseil'")
    
    # Contenu (Page Détail)
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
        # Génère l'URL pour ce projet spécifique
        return reverse('portfolio_detail', kwargs={'pk': self.pk})

# --- Modèles "Inline" liés au Projet ---

class ImageSliderProjet(models.Model):
    """ Images pour le slider sur la page de détail du projet """
    projet = models.ForeignKey(Projet, related_name='images_slider', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projets/slider/')
    legende = models.CharField(max_length=200, blank=True)
    ordre = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['ordre']
        verbose_name = "Image du Slider"

class MetriqueProjet(models.Model):
    """ Métriques (ex: 85%) pour la section 'Impact & Résultats' """
    projet = models.ForeignKey(Projet, related_name='metriques', on_delete=models.CASCADE)
    valeur = models.CharField(max_length=50, help_text="Ex: '85%' ou '500+'")
    label = models.CharField(max_length=100, help_text="Ex: 'Réduction des impacts'")
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Métrique"

class OutilTechnologie(models.Model):
    """ Outils et technologies utilisés pour le projet """
    projet = models.ForeignKey(Projet, related_name='outils', on_delete=models.CASCADE)
    categorie = models.CharField(max_length=100, help_text="Ex: 'Analyses & Mesures', 'Modélisation'")
    nom = models.CharField(max_length=100, help_text="Ex: 'Chromatographie', 'SIG'")
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['categorie', 'ordre']
        verbose_name = "Outil/Technologie"

class ImageProcessusProjet(models.Model):
    """ Images pour la galerie 'Processus d'Étude' """
    projet = models.ForeignKey(Projet, related_name='images_processus', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='projets/processus/')
    legende = models.CharField(max_length=200)
    est_large = models.BooleanField(default=False, help_text="Cochez si cette image doit être plus grande (style 'large')")
    ordre = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['ordre']
        verbose_name = "Image de Processus"

class PointCleProjet(models.Model):
    """ Points clés (icône, titre, texte) pour la page de détail """
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
    """ Modèle pour les membres de l'équipe """
    nom = models.CharField(max_length=200)
    role = models.CharField(max_length=200, help_text="Ex: 'Directeur Scientifique'")
    description = models.TextField(help_text="Courte biographie du membre.")
    image = models.ImageField(upload_to='equipe/', help_text="Photo du membre (de préférence carrée ou ratio 1/1.1)")
    ordre = models.PositiveIntegerField(default=0, help_text="Pour trier l'affichage (le plus petit en premier).")

    # Liens réseaux sociaux (optionnels)
    lien_twitter = models.URLField(blank=True, help_text="Lien complet (URL) vers le profil Twitter/X")
    lien_linkedin = models.URLField(blank=True, help_text="Lien complet (URL) vers le profil LinkedIn")
    email = models.EmailField(blank=True, help_text="Adresse email publique (optionnel)")

    class Meta:
        ordering = ['ordre']
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"

    def __str__(self):
        return self.nom