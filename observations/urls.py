from django.urls import path
from . import views

urlpatterns = [
    path('',              views.accueil,      name='accueil'),
    path('collecte/',     views.collecte,     name='collecte'),
    path('carte/',        views.carte,        name='carte'),
    path('statistiques/', views.statistiques, name='statistiques'),
    path('export/',       views.export,       name='export'),
    path('export/csv/',   views.export_csv,   name='export_csv'),
    path('export/json/',  views.export_json,  name='export_json'),
    path('supprimer/<int:pk>/', views.supprimer, name='supprimer'),
]