from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.db.models import Avg, Min, Max, Count
from .models import Observation
from .forms import ObservationForm
import json
import csv

# ===== ACCUEIL / DASHBOARD =====
def accueil(request):
    observations = Observation.objects.all()
    total        = observations.count()
    regions      = observations.values('region').distinct().count()
    temp_avg     = observations.aggregate(Avg('temp_max'))['temp_max__avg']
    pluie_total  = sum(o.pluie for o in observations if o.pluie)

    # Données pour graphique évolution
    recentes = observations.order_by('date_obs')[:12]
    dates    = [str(o.date_obs) for o in recentes]
    tmax     = [o.temp_max for o in recentes]
    tmin     = [o.temp_min for o in recentes]

    # Données qualité air
    qualites       = ['Bonne', 'Moyenne', 'Mauvaise', 'Très mauvaise']
    qualites_data  = [observations.filter(qualite_air=q).count() for q in qualites]

    # Dernières observations
    dernieres = observations.order_by('-created_at')[:6]

    context = {
        'total':         total,
        'regions':       regions,
        'temp_avg':      round(temp_avg, 1) if temp_avg else '—',
        'pluie_total':   round(pluie_total, 1),
        'dates':         json.dumps(dates),
        'tmax':          json.dumps(tmax),
        'tmin':          json.dumps(tmin),
        'qualites':      json.dumps(qualites),
        'qualites_data': json.dumps(qualites_data),
        'dernieres':     dernieres,
    }
    return render(request, 'observations/accueil.html', context)

# ===== COLLECTE =====
def collecte(request):
    if request.method == 'POST':
        form = ObservationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Observation enregistrée avec succès !')
            return redirect('collecte')
        else:
            messages.error(request, 'Erreur dans le formulaire. Vérifiez les champs.')
    else:
        form = ObservationForm()
    return render(request, 'observations/collecte.html', {'form': form})

# ===== CARTE =====
def carte(request):
    observations = Observation.objects.all()
    regions      = ['Centre','Littoral','Ouest','Nord','Sud','Est','Adamaoua','Nord-Ouest','Sud-Ouest','Extrême-Nord']

    reg_counts   = [observations.filter(region=r).count() for r in regions]
    reg_temps    = []
    for r in regions:
        avg_t = observations.filter(region=r).aggregate(Avg('temp_max'))['temp_max__avg']
        reg_temps.append(round(avg_t, 1) if avg_t else 0)

    context = {
        'regions':    json.dumps(regions),
        'reg_counts': json.dumps(reg_counts),
        'reg_temps':  json.dumps(reg_temps),
        'coverage':   zip(regions, reg_counts),
        'max_count':  max(reg_counts) if reg_counts else 1,
    }
    return render(request, 'observations/carte.html', context)

# ===== STATISTIQUES =====
def statistiques(request):
    observations = Observation.objects.all()

    # Statistiques descriptives
    stats_temp = observations.aggregate(
        avg=Avg('temp_max'), min=Min('temp_max'), max=Max('temp_max')
    )
    stats_tmin = observations.aggregate(
        avg=Avg('temp_min'), min=Min('temp_min'), max=Max('temp_min')
    )
    stats_pluie = observations.aggregate(
        avg=Avg('pluie'), min=Min('pluie'), max=Max('pluie')
    )
    stats_hum = observations.aggregate(
        avg=Avg('humidite'), min=Min('humidite'), max=Max('humidite')
    )
    stats_vent = observations.aggregate(
        avg=Avg('vent'), min=Min('vent'), max=Max('vent')
    )

    # Graphiques
    regions     = ['Centre','Littoral','Ouest','Nord','Sud','Est','Adamaoua','Nord-Ouest','Sud-Ouest','Extrême-Nord']
    pluie_regs  = []
    for r in regions:
        avg_p = observations.filter(region=r).aggregate(Avg('pluie'))['pluie__avg']
        pluie_regs.append(round(avg_p, 1) if avg_p else 0)

    veg_labels  = ['Normal', 'Dégradé', 'Critique']
    veg_data    = [observations.filter(vegetation=v).count() for v in veg_labels]

    pheno_labels = ['Sécheresse', 'Inondation', 'Feux de brousse', 'Érosion', 'Déforestation']
    pheno_data   = [observations.filter(phenomene=p).count() for p in pheno_labels]

    # Dernières temp max pour distribution
    dist_data  = list(observations.order_by('date_obs').values_list('temp_max', flat=True)[:10])
    dist_dates = [str(o.date_obs) for o in observations.order_by('date_obs')[:10]]

    context = {
        'observations':  observations,
        'stats_temp':    stats_temp,
        'stats_tmin':    stats_tmin,
        'stats_pluie':   stats_pluie,
        'stats_hum':     stats_hum,
        'stats_vent':    stats_vent,
        'regions':       json.dumps(regions),
        'pluie_regs':    json.dumps(pluie_regs),
        'veg_labels':    json.dumps(veg_labels),
        'veg_data':      json.dumps(veg_data),
        'pheno_labels':  json.dumps(pheno_labels),
        'pheno_data':    json.dumps(pheno_data),
        'dist_data':     json.dumps(dist_data),
        'dist_dates':    json.dumps(dist_dates),
    }
    return render(request, 'observations/statistiques.html', context)

# ===== EXPORT =====
def export(request):
    observations = Observation.objects.all()
    total        = observations.count()
    regions      = observations.values('region').distinct().count()
    temp_avg     = observations.aggregate(Avg('temp_max'))['temp_max__avg']
    pluie_total  = sum(o.pluie for o in observations if o.pluie)

    context = {
        'total':       total,
        'regions':     regions,
        'temp_avg':    round(temp_avg, 1) if temp_avg else '—',
        'pluie_total': round(pluie_total, 1),
    }
    return render(request, 'observations/export.html', context)

# ===== EXPORT CSV =====
def export_csv(request):
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="climadata_export.csv"'
    response.write('\ufeff')

    writer = csv.writer(response)
    writer.writerow([
        'Date', 'Région', 'Ville', 'Observateur',
        'Temp Min', 'Temp Max', 'Pluie (mm)',
        'Vent (km/h)', 'Humidité (%)',
        'Qualité air', 'Végétation', 'Phénomène', 'Observations'
    ])

    for o in Observation.objects.all():
        writer.writerow([
            o.date_obs, o.region, o.ville, o.observateur,
            o.temp_min, o.temp_max, o.pluie,
            o.vent, o.humidite,
            o.qualite_air, o.vegetation, o.phenomene, o.observations
        ])

    return response

# ===== EXPORT JSON =====
def export_json(request):
    observations = list(Observation.objects.values())
    for o in observations:
        o['date_obs']   = str(o['date_obs'])
        o['created_at'] = str(o['created_at'])
    return JsonResponse(observations, safe=False)

# ===== SUPPRIMER =====
def supprimer(request, pk):
    observation = get_object_or_404(Observation, pk=pk)
    observation.delete()
    messages.success(request, 'Observation supprimée.')
    return redirect('statistiques')