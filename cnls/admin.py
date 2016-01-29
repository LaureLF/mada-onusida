# Register your models here.
#from django.contrib import admin
#Activer l une ou l autre des 2 instruction ci dessous JPN 13/10/2015
from django.contrib.gis import admin
#from leaflet.admin import LeafletGeoAdmin
from cnls.osmgeo_inline import OSMGeoTabularInline


from .models import Organisme, Utilisateur, Action, Typeintervention, Cible, ActionLocalisation, ActionCible, ActionTypeintervention#, Status

## PERMISSIONS (ajout nvx element de la liste) ##

class CibleAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
#        return False
        return True

class TypeinterventionAdmin(admin.ModelAdmin):

    def has_add_permission(self, request, obj=None):
        return True


## SECTIONS  ##

#class ActionCibleAdmin(admin.TabularInline):
class ActionCibleInline(admin.TabularInline):
    model = ActionCible
    extra = 2
    max_num = 3 # TODO Augmenter en production

#class ActionTypeinterventionAdmin(admin.TabularInline):
class ActionTypeinterventionInline(admin.TabularInline):
    model = ActionTypeintervention  
    extra = 2
    max_num = 3 # TODO Augmenter en production

#class ActionLocalisationAdmin(admin.TabularInline):
#class ActionLocalisationInline(admin.TabularInline):
class ActionLocalisationInline(OSMGeoTabularInline):
    model = ActionLocalisation  
    extra = 1
    max_num = 2
    scale_text = False
    openlayers_url = '/static/OpenLayers.js'
    layerswitcher = False
    default_zoom = 3
 #'map_width': 200, 'map_height': 200, 'default_lon': -22, 'default_lat': 43, 'default_zoom': 10, 'layerswitcher': False, 'max_zoom': 15, 'min_zoom': 5, 'scale_text': False, 'debug' = True, }
    # cf. liste des paramètres modifiables https://github.com/django/django/blob/master/django/contrib/gis/admin/options.py
"""    
class ActionLocalisationAdmin(admin.OSMGeoAdmin):
    model = ActionLocalisation
    scale_text = False
    default_zoom = 3
    layerswitcher = False
    openlayers_url = '/static/OpenLayers.js'
#    map_width = 100
#    map_height = 100
    default_lon = -22
    default_lat = 43
"""

        
## L'Admin Principal compose des SECTIONS ##

class ActionAdmin(admin.ModelAdmin):
#class ActionAdmin(admin.OSMGeoAdmin):
    model = Action
    radio_fields = {"echelle_localisation": admin.HORIZONTAL, "devise": admin.HORIZONTAL, "avancement": admin.HORIZONTAL}
#    inlines = [ActionLocalisationInline]#, ActionCibleInline, ActionTypeinterventionInline] # On a agrege les sections
    fieldsets = (
        (u'Informations générales', {
            'fields': ('titre', 'organisme', 'typeintervention', 'cible', 'objectif', 'operateur',),
            'classes': ('wide',),
#            'description': '<i>texte</i>',
        }),
        (u'Localisation', {
            'fields': ('echelle_localisation',),
            'classes': ('wide',),
#            'description': '<i>texte</i>',
        }),
        (u'Période', {
            'fields': ('date_debut', 'date_fin', 'duree', 'avancement'),
            'classes': ('wide',),
#            'description': '<i>texte</i>',
        }),
        (u'Objectifs', {
            'fields': ('objectif', 'priorite_psn', 'resultat_cf_annee_ant',),
            'classes': ('wide',),
#            'description': '<i>texte</i>',
        }),
        (u'Fonds', {
            'fields': (('montant_prevu', 'montant_disponible',), 'devise', 'bailleurfond'),
            'classes': ('wide',),
#            'description': '<i>texte</i>',
        }),
        (u'Contact', {
            'fields': ('createur', 'contact', 'origine'),
            'classes': ('wide',),
#            'description': '<i>texte</i>',
        }),

        (u'Informations avancées', {
            'classes': ('wide',), #'collapse',),
            'fields': ('description', 'commentaire'),
        }),            
    )
    filter_horizontal = ('cible', 'typeintervention')
       

# On enregistre les classes que l'on veut pouvoir modifier depuis l'interface d'administration, suivies éventuellement des modifications de l'interface par défaut

#admin.site.register(mdgRegion, admin.OSMGeoAdmin)
admin.site.register(Organisme)
admin.site.register(Utilisateur)
admin.site.register(Action,ActionAdmin)
#admin.site.register(ActionLocalisation, ActionLocalisationAdmin) #admin.OSMGeoAdmin) #, LeafletGeoAdmin)
admin.site.register(Typeintervention)

#admin.site.register(Status)
admin.site.register(Cible)
