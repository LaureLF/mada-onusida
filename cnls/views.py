#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader
from django.core import serializers
from cnls.geojson_serializer_with_id import GeojsonWithIdSerializer
from django.shortcuts import get_object_or_404 #, render, redirect
from django.db.models import get_model
from django.db.models import Q
#from django.forms.models import model_to_dict
from datetime import datetime
import csv

from cnls.forms import CustomAdminForm
from cnls.models import DICT_ECHELLES, ActionNationale, ActionTananarive, ActionRegionale, ActionLocale, TypeIntervention, Cible

# Create your views here.
def home(request):
#    return redirect('http://cartong.github.io/mada-front/dist/atlas/index.html', permanent=True)
    template = loader.get_template('index.html')
    def to_json(echelle):
        return GeojsonWithIdSerializer().serialize(echelle.objects.filter(validation='valide'), srid='4326', use_natural_foreign_keys=True)
# NB GeojsonWithIdSerializer a été configuré pour ne renvoyer que les champs qui sont utilisés dans le popup - comportement à modifier si besoin dans geojson_serializer_with_id.py
    
    return HttpResponse(template.render(Context({
        'actionsN' : to_json(ActionNationale),
        'actionsT' : to_json(ActionTananarive),
        'actionsR' : to_json(ActionRegionale),
        'actionsL' : to_json(ActionLocale),
        'typesinterventions' : TypeIntervention.objects.all(),
        'cibles' : Cible.objects.all(),        
        })))

def detail(request, classe, id):
    template = loader.get_template('detail.html')
    model = get_model('cnls', classe)
    return HttpResponse(template.render(Context({'action' : get_object_or_404(model.objects.prefetch_related(), pk=id)})))

    
def get_geoactions(request):
    def to_json(echelle):
        return GeojsonWithIdSerializer().serialize(echelle.objects.all(), srid='4326', use_natural_foreign_keys=True)
        #return serializers.serialize('geojson', echelle.objects.all(), srid='4326', use_natural_foreign_keys=True)
    
    data = {
        to_json(ActionNationale),
        to_json(ActionTananarive),
        to_json(ActionRegionale),
        to_json(ActionLocale),
        }
#    data = serializers.serialize('geojson', ActionTananarive.objects.all(), srid='4326', use_natural_foreign_keys=True)
    return HttpResponse(data, content_type='application/json')

#def get_faritra(request):
#    faritra = open(djangoSettings.STATIC_ROOT + 'json/faritra.json', 'r')
#    #faritra = serializers.serialize('json', data)
#    return HttpResponse(faritra)


def export_csv(request, ids=None):  
    params = request.GET.getlist('id', default=None)
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="CNLS_selection.csv"'

    writer = csv.writer(response)
    writer.writerow(["Titre", "Description", "Organisme maître d'œuvre", "Types d'interventions", "Publics cibles", "Echelle", "Localisation", "Coordonnées géographiques", "Date de démarrage", "Date de fin", "Durée de l'action", "Etat d'avancement", "Nombre de personnes visées", "Opérateur en lien avec l'action", "Priorité du PSN que l'activité appuie", "Résultat par rapport à l'année précédente", "Montant prévu", "Montant disponible", "Devise", "Bailleur de fond", "Origine de la donnée", "Commentaires", "Nom du responsable de la fiche", "Fiche créée le", "Dernière modification le"])
    echelles = request.GET.getlist('e', '')
    if echelles:
        #try:
        cibles = Cible.objects.all().filter(nom__in = request.GET.getlist('c', ''))
        #except Cible.empty:
        #pass
        types = TypeIntervention.objects.all().filter(nom__in = request.GET.getlist('t', ''))
        for echelle in echelles:
            model = get_model('cnls', echelle)
            champ_localisation = DICT_ECHELLES[model.__name__]['champ']
            queryset = model.objects.all().filter(validation='valide').filter(typeintervention__in = types).filter(Q(date_debut__lte = datetime.strptime(request.GET.get('f'), '%Y-%m-%d').date()) | Q(date_debut__isnull=True)).filter(Q(date_fin__gte = datetime.strptime(request.GET.get('d'), '%Y-%m-%d').date()) | Q(date_fin__isnull=True))
            

            for action in queryset:
                test = getattr(action, champ_localisation).all()
                writer.writerow([
                    action.titre, 
                    action.description, 
                    action.organisme, 
                    ', '.join([str(t) for t in action.typeintervention.all()]), 
                    ', '.join([str(c) for c in action.cible.all()]), 
                    DICT_ECHELLES[model.__name__]['adj_fr'], 
                    ', '.join([str(l) for l in getattr(action, champ_localisation).all()]), 
                    action.mpoint, 
                    action.date_debut, 
                    action.date_fin, 
                    action.duree, 
                    action.avancement, 
                    action.objectif, 
                    action.operateur, 
                    action.priorite_psn, 
                    action.resultat_cf_annee_ant, 
                    action.montant_prevu, 
                    action.montant_disponible, 
                    action.devise, 
                    action.bailleur, 
                    action.origine, 
                    action.commentaire, 
                    action.createur, 
                    action.creation, 
                    action.maj
                ])
           
    # normalement ce cas n'est pas rencontré car filtré par le JavaScript mais au cas où une URL serait écrite à la main:
    else:
        return
    return response
    
def apropos(request):
    template = loader.get_template('apropos.html')
    return HttpResponse(template.render())

