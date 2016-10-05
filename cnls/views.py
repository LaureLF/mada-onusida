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

####################
# La page d'accueil du site (index.html)
def home(request):
#    return redirect('http://cartong.github.io/mada-front/dist/atlas/index.html', permanent=True)
    template = loader.get_template('cnls/index.html')
    def to_json(echelle):
        # Convertit en GeoJson les actions validées par un administrateur, grâce au "serializer" personnalisé de geojson_serializer_with_id.py
        return GeojsonWithIdSerializer().serialize(echelle.objects.filter(validation='valide'), srid='4326', use_natural_foreign_keys=True)
        # NB GeojsonWithIdSerializer a été configuré pour ne renvoyer que les champs qui sont utilisés dans le popup - comportement à modifier si besoin dans geojson_serializer_with_id.py

    # Données envoyées à index.html, comprenant les différents niveaux d'échelle, les cibles et types d'intervention (pour les filtres)
    return HttpResponse(template.render(Context({
        'actionsN' : to_json(ActionNationale),
        'actionsT' : to_json(ActionTananarive),
        'actionsR' : to_json(ActionRegionale),
        'actionsL' : to_json(ActionLocale),
        'typesinterventions' : TypeIntervention.objects.all(),
        'cibles' : Cible.objects.all(),
        })))

####################
# Page de détail d'une action dont la primary key est id
def detail(request, classe, id):
    template = loader.get_template('cnls/detail.html')
    model = get_model('cnls', classe)
    # Si l'id n'est pas trouvé dans la classe, renvoie une erreur 404 (not found)
    return HttpResponse(template.render(Context({'action' : get_object_or_404(model.objects.prefetch_related(), pk=id)})))

####################
# Page renvoyant au format texte le GeoJson correpondant à la base de données
# NB à des fins de test seulement, TODO à supprimer à terme ou u moins à filtrer sur les actions validées
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

####################
# Pour quand on aura la géographie des nouvelles régions
#def get_faritra(request):
#    faritra = open(djangoSettings.STATIC_ROOT + 'json/faritra.json', 'r')
#    #faritra = serializers.serialize('json', data)
#    return HttpResponse(faritra)

####################
# Crée le fichier CSV d'export
def export_csv(request, ids=None):  
    # On récupère l'id transmise par l'url (parmi les paramètres après le ?
    params = request.GET.getlist('id', default=None)
    response = HttpResponse(content_type='text/csv')
    # Le fichier téléchargé par l'utilisateur d'appelera CNLS_selection.csv
    response['Content-Disposition'] = 'attachment; filename="CNLS_selection.csv"'

    writer = csv.writer(response)
    # On crée les colonnes correspondants aux champs qui seront exportés
    writer.writerow(["Titre", "Description", "Organisme maître d'œuvre", "Types d'interventions", "Publics cibles", "Echelle", "Localisation", "Coordonnées géographiques", "Date de démarrage", "Date de fin", "Durée de l'action", "Etat d'avancement", "Nombre de personnes visées", "Opérateur en lien avec l'action", "Priorité du PSN que l'activité appuie", "Résultat par rapport à l'année précédente", "Montant prévu", "Montant disponible", "Devise", "Bailleur de fond", "Origine de la donnée", "Commentaires", "Nom du responsable de la fiche", "Fiche créée le", "Dernière modification le"])
    # On récupère les échelles transmise par l'url (paramètre e après le ?
    echelles = request.GET.getlist('e', '')
    if echelles:
        #try:
        # On récupère les cibles (paramètre c) passées par l'url
        cibles = Cible.objects.all().filter(nom__in = request.GET.getlist('c', ''))
        #except Cible.empty:
        #pass
        # On récupère les types d'intervention (paramètre t) passés par l'url
        types = TypeIntervention.objects.all().filter(nom__in = request.GET.getlist('t', ''))
        for echelle in echelles:
            model = get_model('cnls', echelle)
            champ_localisation = DICT_ECHELLES[model.__name__]['champ']
            # On récupère les objets de la base de données validant les différents filtres
            queryset = model.objects.all().filter(validation='valide').filter(typeintervention__in = types).filter(Q(date_debut__lte = datetime.strptime(request.GET.get('f'), '%Y-%m-%d').date()) | Q(date_debut__isnull=True)).filter(Q(date_fin__gte = datetime.strptime(request.GET.get('d'), '%Y-%m-%d').date()) | Q(date_fin__isnull=True))
            
            # On écrit une ligne par objet dans le CSV
            for action in queryset:
                test = getattr(action, champ_localisation).all()
                # Pour l'objet considéré, on écrit les valeurs des différentes colonnes dans le même ordre que les colonnes définies ci-dessous
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

####################    
# La page À propos
def apropos(request):
    template = loader.get_template('apropos.html')
    return HttpResponse(template.render())
