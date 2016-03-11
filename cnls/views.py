#-*- coding: utf-8 -*-
from django.http import HttpResponse
from django.template import Context, loader
from django.core import serializers
from django.shortcuts import get_object_or_404 #, render, redirect
from django.db.models import get_model
#from django.conf import settings as djangoSettings

from .models import ActionNationale, ActionTananarive, ActionRegionale, ActionLocale, TypeIntervention, Cible

# Create your views here.
def home(request):
#    return redirect('http://cartong.github.io/mada-front/dist/atlas/index.html', permanent=True)
    template = loader.get_template('index.html')
    def to_json(echelle):
        return serializers.serialize('geojson', echelle.objects.all(), srid='4326', use_natural_foreign_keys=True)
    
    return HttpResponse(template.render(Context({
        'actionsN' : to_json(ActionNationale),
        'actionsT' : to_json(ActionTananarive),
        'actionsR' : to_json(ActionRegionale),
        'actionsL' : to_json(ActionLocale),
        'typesinterventions' : TypeIntervention.objects.all(),
        'cibles' : Cible.objects.all(),        
        })))

def detail(request, action_echelle, action_id):
    template = loader.get_template('detail.html')
    model = get_model('cnls', action_echelle)
#    return HttpResponse("%s n° %s." % (action_echelle, action_id))
    return HttpResponse(template.render(Context({'action' : get_object_or_404(model, pk=action_id)})))
    
# inusité
def get_geoactions(request):
    actions = ActionLocale.objects.all()
    data = serializers.serialize('geojson', actions, srid='4326', use_natural_foreign_keys=True)
    return HttpResponse(data, content_type='application/json')

#def get_faritra(request):
#    faritra = open(djangoSettings.STATIC_ROOT + 'json/faritra.json', 'r')
#    #faritra = serializers.serialize('json', data)
#    return HttpResponse(faritra)
