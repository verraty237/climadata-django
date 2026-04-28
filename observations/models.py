from django.db import models

class Observation(models.Model):

    REGIONS = [
        ('Centre', 'Centre'),
        ('Littoral', 'Littoral'),
        ('Ouest', 'Ouest'),
        ('Nord', 'Nord'),
        ('Sud', 'Sud'),
        ('Est', 'Est'),
        ('Adamaoua', 'Adamaoua'),
        ('Nord-Ouest', 'Nord-Ouest'),
        ('Sud-Ouest', 'Sud-Ouest'),
        ('Extrême-Nord', 'Extrême-Nord'),
    ]

    QUALITE_AIR = [
        ('Bonne', 'Bonne'),
        ('Moyenne', 'Moyenne'),
        ('Mauvaise', 'Mauvaise'),
        ('Très mauvaise', 'Très mauvaise'),
    ]

    VEGETATION = [
        ('Normal', 'Normal'),
        ('Dégradé', 'Dégradé'),
        ('Critique', 'Critique'),
    ]

    PHENOMENES = [
        ('Sécheresse', 'Sécheresse'),
        ('Inondation', 'Inondation'),
        ('Feux de brousse', 'Feux de brousse'),
        ('Érosion', 'Érosion'),
        ('Déforestation', 'Déforestation'),
    ]

    # Localisation
    region      = models.CharField(max_length=50, choices=REGIONS)
    ville       = models.CharField(max_length=100)
    date_obs    = models.DateField()
    observateur = models.CharField(max_length=100, blank=True, null=True)

    # Météo
    temp_min    = models.FloatField(blank=True, null=True)
    temp_max    = models.FloatField(blank=True, null=True)
    pluie       = models.FloatField(blank=True, null=True)
    vent        = models.FloatField(blank=True, null=True)
    humidite    = models.FloatField(blank=True, null=True)
    qualite_air = models.CharField(max_length=20, choices=QUALITE_AIR, blank=True, null=True)

    # Environnement
    vegetation   = models.CharField(max_length=20, choices=VEGETATION, blank=True, null=True)
    phenomene    = models.CharField(max_length=30, choices=PHENOMENES, blank=True, null=True)
    observations = models.TextField(blank=True, null=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Observation'
        verbose_name_plural = 'Observations'

    def __str__(self):
        return f"{self.region} - {self.ville} - {self.date_obs}"