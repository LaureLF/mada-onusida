from django.contrib.gis import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from datetime import datetime
from leaflet.admin import LeafletGeoAdmin
from cnls.forms import CustomUserCreationForm, CustomUserChangeForm, CustomAdminForm
from cnls.models import Organisme, Bailleur, Action, TypeIntervention, Cible, ActionTananarive, ActionNationale, ActionRegionale, ActionLocale, Faritra, Kaominina, Fokontany, Profil
     

class ActionAdmin(LeafletGeoAdmin):
    map_width = '80%'
    map_height = '400px'
    display_raw = False

    form = CustomAdminForm
    radio_fields = {"devise": admin.HORIZONTAL, "avancement": admin.HORIZONTAL}

    class Meta:
        abstract = True
        
    def is_admin(self, instance):
        return request.user.is_superuser
    
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ['createur']

    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.creation = datetime.now()
            obj.slug = slugify(obj.titre)
        if not request.user.is_superuser:
            obj.createur = request.user
        obj.maj = datetime.now()
        obj.login_maj = request.user
        super(ActionAdmin, self).save_model(request, obj, form, change)

    def ordre_fieldsets(description, nom_localisation):
        fieldsets = []
        fieldsets.append(        
            (u'Informations générales', {
                'fields': ('titre', 'description', 'organisme', 'typeintervention', 'cible',),
                'classes': ('wide',),
                'description': "<i><p>L'action sera symbolisée par un marqueur de couleur " + description + ".</p><p>NB. Pour enregistrer des actions à d'autres échelles, veuillez retourner à la page d'accueil.</i>", 
                })     
        )
        if (nom_localisation is not None):
            fieldsets.append(
            (u'Localisation', {
                'fields': ('mpoint', 'mpoint_text', nom_localisation),
                'classes': ('wide',),
                'description': '<i><p>Vous pouvez renseigner une ou plusieurs localisations de cette action,</p><p>en utilisant soit la carte soit les coordonnées GPS (système géodésique WGS 84), mais pas les deux.</p></i>',
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
            (u'Objectifs et moyens', {
                'fields': ('objectif', 'operateur', 'priorite_psn', 'resultat_cf_annee_ant', ('montant_prevu', 'montant_disponible',), 'devise', 'bailleur'),
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
                'classes': ('wide',), #, 'collapse',),
                'fields': ('commentaire', ),
            })
        )
        return tuple(fieldsets)
            
class ActionNationaleAdmin(ActionAdmin):
    fieldsets = ActionAdmin.ordre_fieldsets("sur la capitale", None) 
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention')
        
    def save_model(self, request, obj, form, change):
        obj.mpoint = GEOSPoint(-18.933333, 47.516667, srid=4326)
# tester obj.mpoint = obj.TANANARIVE
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
admin.site.register(Bailleur)
#admin.site.register(Profil)
admin.site.register(ActionNationale,ActionNationaleAdmin)
admin.site.register(ActionTananarive,ActionTananariveAdmin)
admin.site.register(ActionRegionale,ActionRegionaleAdmin)
admin.site.register(ActionLocale,ActionLocaleAdmin)
admin.site.register(TypeIntervention)
admin.site.register(Cible)
admin.site.register(Faritra)
admin.site.register(Kaominina)
admin.site.register(Fokontany)

###########################
class ProfilInline(admin.StackedInline):
    max_number = 1
    model = Profil
    fields = ('organisme','poste','photo')
    can_delete = False
    verbose_name_plural = 'Données professionnelles'
  
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    add_fieldsets = (
        (None, {'fields': ('username', 'email', 'password1', 'password2')}),)
    form = CustomUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', ('first_name', 'last_name'))}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'groups', )}), 
    )
    filter_horizontal = ()

    def add_view(self, *args, **kwargs):
      self.inlines = []
      return super(CustomUserAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
      self.inlines = (ProfilInline,)
      return super(CustomUserAdmin, self).change_view(*args, **kwargs)
    
    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super(CustomUserAdmin, self).save_model(request, obj, form, change)
        
# unregister any existing admin for the User model and register mine
try:
    admin.site.unregister(User)
except NotRegistered:
    pass
admin.site.register(User, CustomUserAdmin)