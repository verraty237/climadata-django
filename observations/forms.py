from django import forms
from .models import Observation

class ObservationForm(forms.ModelForm):

    class Meta:
        model  = Observation
        fields = [
            'region', 'ville', 'date_obs', 'observateur',
            'temp_min', 'temp_max', 'pluie', 'vent', 'humidite',
            'qualite_air', 'vegetation', 'phenomene', 'observations'
        ]
        widgets = {
            'region': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': '— Sélectionner —'
            }),
            'ville': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: Yaoundé'
            }),
            'date_obs': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'observateur': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Votre nom'
            }),
            'temp_min': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 18',
                'step': '0.1'
            }),
            'temp_max': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 32',
                'step': '0.1'
            }),
            'pluie': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 45',
                'step': '0.1'
            }),
            'vent': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 12',
                'step': '0.1'
            }),
            'humidite': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: 75',
                'min': '0',
                'max': '100'
            }),
            'qualite_air': forms.Select(attrs={
                'class': 'form-control'
            }),
            'vegetation': forms.Select(attrs={
                'class': 'form-control'
            }),
            'phenomene': forms.Select(attrs={
                'class': 'form-control'
            }),
            'observations': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Décrivez ce que vous avez observé...',
                'rows': '3'
            }),
        }
        labels = {
            'region':       'Région *',
            'ville':        'Ville / Localité *',
            'date_obs':     "Date d'observation *",
            'observateur':  'Observateur',
            'temp_min':     'Température min (°C)',
            'temp_max':     'Température max (°C)',
            'pluie':        'Pluviométrie (mm)',
            'vent':         'Vitesse du vent (km/h)',
            'humidite':     'Humidité (%)',
            'qualite_air':  "Qualité de l'air",
            'vegetation':   'État de la végétation',
            'phenomene':    'Phénomène observé',
            'observations': 'Observations libres',
        }