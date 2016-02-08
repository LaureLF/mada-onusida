# Register your models here.
from django.contrib.gis import admin

from .models import Organisme, Utilisateur, Action, Typeintervention, Cible, ActionTananarive, ActionNationale, ActionRegionale, ActionLocale, Region, Commune, Fokontany

## SECTIONS  ##       

class ActionAdmin(admin.ModelAdmin):
    radio_fields = {"devise": admin.HORIZONTAL, "avancement": admin.HORIZONTAL}
#    filter_horizontal = ('cible', 'typeintervention')
    readonly_fields= ('echelle_localisation', 'mpoint')

    class Meta:
        abstract = True
    
    def ordre_fieldsets(nom_localisation, description):
        fieldsets = (
        (u'Informations générales', {
            'fields': ('titre', 'description', 'organisme', 'typeintervention', 'cible', 'objectif', 'operateur',),
            'classes': ('wide',),
        }),     
        (u'Localisation', {
            'fields': ('echelle_localisation', ('latitude', 'longitude',), nom_localisation),
            'classes': ('wide',),
            'description': "<i><p>L'action sera symbolisée par un marqueur de couleur " + description + ".</p><p>NB. Pour enregistrer des actions à d'autres échelles, veuillez retourner à la page d'accueil.</i>", 
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
            'fields': ('commentaire',),
        }),            
    )
        return fieldsets
            
class ActionNationaleAdmin(ActionAdmin):
    fieldsets = ActionAdmin.ordre_fieldsets("", "sur la capitale") # TODO ou un point dans la mer ? # TODO préciser couleur
    model = ActionTananarive

class ActionTananariveAdmin(ActionAdmin):
    fieldsets = ActionAdmin.ordre_fieldsets("fokontany", "sur la capitale") # TODO préciser couleur
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention', 'fokontany')

class ActionRegionaleAdmin(ActionAdmin):
    fieldsets = ActionAdmin.ordre_fieldsets("region", "sur la capitale de région") # TODO préciser couleur
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention', 'region')

class ActionLocaleAdmin(ActionAdmin):
    fieldsets = ActionAdmin.ordre_fieldsets("commune", "sur la commune") # TODO préciser couleur
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention', 'commune')

# On enregistre les classes que l'on veut pouvoir modifier depuis l'interface d'administration, suivies éventuellement des modifications de l'interface par défaut

#admin.site.register(mdgRegion, admin.OSMGeoAdmin)
admin.site.register(Organisme)
admin.site.register(Utilisateur)
admin.site.register(ActionNationale,ActionNationaleAdmin)
admin.site.register(ActionTananarive,ActionTananariveAdmin)
admin.site.register(ActionRegionale,ActionRegionaleAdmin)
admin.site.register(ActionLocale,ActionLocaleAdmin)
admin.site.register(Typeintervention)
admin.site.register(Cible)
admin.site.register(Region)
admin.site.register(Commune)
admin.site.register(Fokontany)