from django.urls import path
from . import views

# Ces noms (ex: 'index') sont ceux que nous utilisons dans les templates {% url '...' %}
urlpatterns = [
    # URLs des pages principales
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    
    # URLs du Portfolio
    path('portfolio/', views.portfolio_list, name='portfolio_list'),
    path('portfolio/<int:pk>/', views.portfolio_detail, name='portfolio_detail'),
    
    # URL de Contact
    path('contact/', views.contact, name='contact'),
    
    # URLs pour les actions de formulaire (POST)
    path('newsletter-signup/', views.newsletter_signup, name='newsletter_signup'),
]