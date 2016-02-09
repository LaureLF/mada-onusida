#-*- coding: utf-8 -*-

#from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import Context, loader
from django.core import serializers
from django.conf import settings as djangoSettings

from .models import ActionNationale, ActionTananarive, ActionRegionale, ActionLocale

# !! les noms des class models devraient commencer par une Majuscule !!

# Create your views here.
"""
def home(request):
    return redirect('http://cartong.github.io/mada-front/dist/atlas/index.html', permanent=True)"""
def home(request):
    template = loader.get_template('index.html')
#    return HttpResponse(template.render())
#    actionlocalisations = ActionLocalisation.objects.all()
#    context = Context({'data' : actionlocalisations})
#    return HttpResponse(template.render(context))
    def to_json(echelle):
        return serializers.serialize('geojson', echelle.objects.all(), srid='4326', use_natural_foreign_keys=True)
        
    return HttpResponse(template.render(Context({
        'actionsN' : to_json(ActionNationale),
        'actionsT' : to_json(ActionTananarive),
        'actionsR' : to_json(ActionRegionale),
        'actionsL' : to_json(ActionLocale)})))

"""
def get_actions(request):
    actions = Action.objects.all()
    data = serializers.serialize('json', actions)
    return HttpResponse(data)
    
def get_actions_by_title(request, title):
    actions = Action.objects.filter(titre=title)
    data = serializers.serialize('json', actions)
    return HttpResponse(data)    
"""
def get_geoactions(request):
#    actions = ActionLocalisation.objects.all()
    actions = ActionRegionale.objects.all()
    data = serializers.serialize('geojson', actions, srid='4326', use_natural_foreign_keys=True)
    return HttpResponse(data, content_type='application/json')
"""
def api_action(request, id):
    if request.method == 'GET':
        action = Action.objects.get(pk=id)
        data = serializers.serialize('geojson', action)
        return HttpResponse(data)
    elif request.method == 'POST':
        action = Action.objects.get(pk=id)
        action.title = request.post.title
        action.description = request.post.description
        action.save()
        return HttpResponse('OK')    
"""
#def get_faritra(request):
#    faritra = open(djangoSettings.STATIC_ROOT + 'json/faritra.json', 'r')
#    #faritra = serializers.serialize('json', data)
#    return HttpResponse(faritra)
