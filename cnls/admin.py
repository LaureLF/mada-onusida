# Register your models here.
from django.contrib.gis import admin
from leaflet.admin import LeafletGeoAdmin
from cnls.models import Organisme, Utilisateur, Action, TypeIntervention, Cible, ActionTananarive, ActionNationale, ActionRegionale, ActionLocale, Faritra, Kaominina, Fokontany

## SECTIONS  ##       

#class ActionAdmin(admin.ModelAdmin):
class ActionAdmin(LeafletGeoAdmin):
    map_width = '80%'
    map_height = '500px'
    display_raw = False

    radio_fields = {"devise": admin.HORIZONTAL, "avancement": admin.HORIZONTAL}
#    readonly_fields= ('echelle_localisation', 'mpoint')

    class Meta:
        abstract = True
    
#    def save_model(self, request, obj, form, change):
#        obj.save()
#        form.save_m2m()
#        obj.mpoint = GEOSMultiPoint([reg.mpoint for reg in getattr(obj, self.ECHELLE).all()])
#        super(ActionAdmin, self).save_model(request, obj, form, change)

    def ordre_fieldsets(description, nom_localisation):
        fieldsets = []
        fieldsets.append(        
            (u'Informations générales', {
                'fields': ('titre', 'description', 'organisme', 'typeintervention', 'cible', 'objectif', 'operateur',),
                'classes': ('wide',),
                'description': "<i><p>L'action sera symbolisée par un marqueur de couleur " + description + ".</p><p>NB. Pour enregistrer des actions à d'autres échelles, veuillez retourner à la page d'accueil.</i>", 
                })     
        )
        if (nom_localisation is not None):
            fieldsets.append(
            (u'Localisation', {
#            'fields': ('echelle_localisation', ('latitude', 'longitude',), nom_localisation), # latitudes et longitudes multiples pour l'instant non gérés
                'fields': ('mpoint', nom_localisation),
                'classes': ('wide',),
            })
        )
        fieldsets.append(
            (u'Période', {
                'fields': ('date_debut', 'date_fin', 'duree', 'avancement'),
                'classes': ('wide',),
#                'description': '<i>texte</i>',
            })
        )
        fieldsets.append(
            (u'Objectifs', {
                'fields': ('objectif', 'priorite_psn', 'resultat_cf_annee_ant',),
                'classes': ('wide',),
#                'description': '<i>texte</i>',
            })
        )
        fieldsets.append(
            (u'Fonds', {
                'fields': (('montant_prevu', 'montant_disponible',), 'devise', 'bailleurfond'),
                'classes': ('wide',),
#                'description': '<i>texte</i>',
            })
        )
        fieldsets.append(
            (u'Contact', {
                'fields': ('createur', 'contact', 'origine'),
                'classes': ('wide',),
#                'description': '<i>texte</i>',
            })
        )
        fieldsets.append(
            (u'Informations avancées', {
                'classes': ('wide',), #'collapse',),
                'fields': ('commentaire',),
            })
        )
        return tuple(fieldsets)
            
class ActionNationaleAdmin(ActionAdmin):
    fieldsets = ActionAdmin.ordre_fieldsets("sur la capitale", None) # TODO ou un point dans la mer ? # TODO préciser couleur
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention')
        
    def save_model(self, request, obj, form, change):
        obj.mpoint = GEOSPoint(-18.933333, 47.516667, srid=4326)
        super(ActionNationaleAdmin, self).save_model(request, obj, form, change)

class ActionTananariveAdmin(ActionAdmin):
    ECHELLE = 'fokontany'
    fieldsets = ActionAdmin.ordre_fieldsets("sur la capitale", ECHELLE) # TODO préciser couleur
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention', ECHELLE)

class ActionRegionaleAdmin(ActionAdmin):
    ECHELLE = 'region'
    fieldsets = ActionAdmin.ordre_fieldsets("sur la capitale de région", ECHELLE) # TODO préciser couleur
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention', ECHELLE)

class ActionLocaleAdmin(ActionAdmin):
    ECHELLE = 'commune'
    fieldsets = ActionAdmin.ordre_fieldsets("sur la commune", ECHELLE) # TODO préciser couleur
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention', ECHELLE)

# On enregistre les classes que l'on veut pouvoir modifier depuis l'interface d'administration, suivies éventuellement des modifications de l'interface par défaut

admin.site.register(Organisme)
admin.site.register(Utilisateur)
admin.site.register(ActionNationale,ActionNationaleAdmin)
admin.site.register(ActionTananarive,ActionTananariveAdmin)
admin.site.register(ActionRegionale,ActionRegionaleAdmin)
admin.site.register(ActionLocale,ActionLocaleAdmin)
admin.site.register(TypeIntervention)
admin.site.register(Cible)
admin.site.register(Faritra)
admin.site.register(Kaominina)
admin.site.register(Fokontany)