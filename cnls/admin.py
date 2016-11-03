from django.contrib.gis import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from datetime import datetime
from leaflet.admin import LeafletGeoAdmin
from cnls.forms import CustomUserCreationForm, CustomUserChangeForm, CustomAdminForm
from cnls.models import Organisme, Bailleur, Action,  ActionTananarive, ActionNationale, ActionRegionale, ActionLocale,  Profil, ActionNationaleAValider, ActionTananariveAValider, ActionRegionaleAValider, ActionLocaleAValider #, TypeIntervention, Cible, Faritra, Kaominina, Fokontany
from feedback.models import Feedback

###################
# Titre du site et de diverses sections
###################
admin.site.site_title = 'Atlas CNLS' # Text to put at the end of each page's <title>.
admin.site.site_header = 'Application CNLS - Administration' # Text to put in each page's <h1>.
admin.site.index_title = 'Gestion des actions de lutte contre le SIDA' # Text to put at the top of the admin index page.
#admin.site.site_url = None # Remove the "View on site" link from the admin change view

###################
# Pages d'administration pour les modèles Action (abstraite + 4 échelles)
###################
class ActionAdmin(LeafletGeoAdmin):
    map_width = '80%'
    map_height = '400px'
    display_raw = False

    # Utilisation d'un formulaire adapté, défini dans le fichier forms.py
    form = CustomAdminForm
    # Radio buttons à afficher horizontalement (par défaut les choix sont présentés verticalement)
    radio_fields = {"devise": admin.HORIZONTAL, "avancement": admin.HORIZONTAL, "validation": admin.HORIZONTAL}

    # ActionAdmin est une classe abstraite réunissant les paramètres communs des 4 modèles d'actions par échelles
    class Meta:
        abstract = True

    # Fonction pour vérifier le statut administrateur d'un utilisateur
    def is_admin(self, instance):
        return request.user.is_superuser

    # Fonction pour rendre certains champs non modifiables par les non administrateurs
    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        return ['createur', 'validation']

    # Personnalisation de la fonction qui enregistre les actions pour y ajouter des champs non accessibles aux utilisateurs
    def save_model(self, request, obj, form, change):
        if not obj.id:
            obj.creation = datetime.now()
            obj.slug = slugify(obj.titre)
        else:
            obj.maj = datetime.now()
            obj.login_maj = request.user
        if not request.user.is_superuser:
            obj.createur = request.user
        super(ActionAdmin, self).save_model(request, obj, form, change)

    # Fonction qui définit l'ordre et la présentation des champs.
    # description et nom_localisation viennent des sous classes par échelle
    def ordre_fieldsets(description, nom_localisation):
        fieldsets = []
        fieldsets.append(
            (u'Informations générales', {
                'fields': ('titre', 'description', 'validation', 'organisme', 'typeintervention', 'cible',),
                'classes': ('wide',),
                'description': "<i><p>L'action sera symbolisée par un marqueur de couleur " + description + ".</p><p>NB. Pour enregistrer des actions à d'autres échelles, veuillez retourner à la page d'accueil.</i>", 
                })
        )
        # Cette section n'existe pas pour les actions nationales (que l'utilisateur n'a pas à localiser sur une carte)
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

###################
class ActionNationaleAdmin(ActionAdmin):
    fieldsets = ActionAdmin.ordre_fieldsets("sur la capitale", None) 
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention')

    # L'action est positionnée sur la capitale
    def save_model(self, request, obj, form, change):
        obj.mpoint = GEOSPoint(-18.933333, 47.516667, srid=4326)
# tester obj.mpoint = obj.TANANARIVE
        super(ActionNationaleAdmin, self).save_model(request, obj, form, change)

###################
class ActionTananariveAdmin(ActionAdmin):
    ECHELLE = 'fokontany'
    fieldsets = ActionAdmin.ordre_fieldsets("sur la capitale", ECHELLE) # TODO préciser couleur
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention', ECHELLE)

###################
class ActionRegionaleAdmin(ActionAdmin):
    ECHELLE = 'region'
    fieldsets = ActionAdmin.ordre_fieldsets("sur la capitale de région", ECHELLE) # TODO préciser couleur
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention', ECHELLE)

###################
class ActionLocaleAdmin(ActionAdmin):
    ECHELLE = 'commune'
    fieldsets = ActionAdmin.ordre_fieldsets("sur la commune", ECHELLE) # TODO préciser couleur
    model = ActionTananarive
    filter_horizontal = ('cible', 'typeintervention', ECHELLE)


###################
# Pages d'administration pour les modèles Action pas encore validés (4 modèles virtuels ou "proxy" du fichier models.py)
###################

class ActionNationaleAValiderAdmin(ActionNationaleAdmin):
    # Fonction qui n'affiche que les actions nationales pas encore validées par un administrateur,
    # l'affichage étant identique à ActionNationaleAdmin
    def get_queryset(self, request):
        qs = super(ActionNationaleAdmin, self).get_queryset(request)
        qs = qs.filter(validation='pasencore')
        return qs

###################
class ActionTananariveAValiderAdmin(ActionTananariveAdmin):
    # Fonction qui n'affiche que les actions à Tananarive pas encore validées par un administrateur,
    # l'affichage étant identique à ActionTananariveAdmin
    def get_queryset(self, request):
        qs = super(ActionTananariveAdmin, self).get_queryset(request)
        qs = qs.filter(validation='pasencore')
        return qs

###################
class ActionRegionaleAValiderAdmin(ActionRegionaleAdmin):
    # Fonction qui n'affiche que les actions préfectorales/régionales pas encore validées par un administrateur,
    # l'affichage étant identique à ActionRegionaleAdmin
    def get_queryset(self, request):
        qs = super(ActionRegionaleAdmin, self).get_queryset(request)
        qs = qs.filter(validation='pasencore')
        return qs

###################
class ActionLocaleAValiderAdmin(ActionLocaleAdmin):
    # Fonction qui n'affiche que les actions locales pas encore validées par un administrateur,
    # l'affichage étant identique à ActionLocaleAdmin
    def get_queryset(self, request):
        qs = super(ActionLocaleAdmin, self).get_queryset(request)
        qs = qs.filter(validation='pasencore')
        return qs


###################
# Enregistrement des classes accessibles depuis l'interface d'administration 
# (suivies éventuellement des modifications de l'interface par défaut)
###################
admin.site.register(Organisme)
admin.site.register(Bailleur)
#admin.site.register(Profil)
admin.site.register(ActionNationale,ActionNationaleAdmin)
admin.site.register(ActionTananarive,ActionTananariveAdmin)
admin.site.register(ActionRegionale,ActionRegionaleAdmin)
admin.site.register(ActionLocale,ActionLocaleAdmin)
#admin.site.register(TypeIntervention)
#admin.site.register(Cible)
#admin.site.register(Faritra)
#admin.site.register(Kaominina)
#admin.site.register(Fokontany)
admin.site.register(ActionNationaleAValider, ActionNationaleAValiderAdmin)
admin.site.register(ActionTananariveAValider, ActionTananariveAValiderAdmin)
admin.site.register(ActionRegionaleAValider, ActionRegionaleAValiderAdmin)
admin.site.register(ActionLocaleAValider, ActionLocaleAValiderAdmin)
admin.site.register(Feedback)

###################
# Cas spécifique de la gestion des utilisateurs (classe User de Django et Profile de models.py)
###################
# Les champs propres au projet CNLS (modèle Profile) seront rajoutés sous forme de composant Inline à la fin des champs de User
class ProfilInline(admin.StackedInline):
    max_number = 1
    model = Profil
    fields = ('organisme','poste','photo')
    can_delete = False
    verbose_name_plural = 'Données professionnelles'

# Le fonctionnement en 2 écrans successifs (add_view puis change_view dans la foulée) vient de la classe User de Django
# mais pose des problèmes pour les champs obligatoires de Profile (NB non résolu)
class CustomUserAdmin(UserAdmin):
    # Premier écran : les informations de base et de connexion
    add_form = CustomUserCreationForm
    # Les champs qu'on veut sur le premier écran d'enregistrement d'un utilisateur
    add_fieldsets = (
        (None, {'fields': ('username', ('first_name', 'last_name'), 'email', 'password1', 'password2') }),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'groups', )}),
        (_('Données professionnelles'), {'fields': ('organisme', 'poste', 'photo', )}),
        )
    # Second écran : informations plus détaillées
    form = CustomUserChangeForm
    # Les champs qu'on veut sur le second écran d'enregistrement d'un utilisateur
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', ('first_name', 'last_name'))}),
        (_('Permissions'), {'fields': ('is_active', 'is_superuser', 'groups', )}),
        # Les données du modèle Profil sont chargées dans le ProfilInline
    )
    filter_horizontal = ('groups',)

    def get_form(self, request, obj, **kwargs):
        form = super(CustomUserAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['username'].label = 'Identifiant'
        form.base_fields['is_active'].label = 'Compte en activité'
        form.base_fields['is_superuser'].label = 'Statut administrateur'
        form.base_fields['groups'].label = 'Niveau de responsabilités'
#        form.base_fields['is_superuser'].help_text = 'My help text'
        return form

    def add_view(self, *args, **kwargs):
      self.inlines = []
      return super(CustomUserAdmin, self).add_view(*args, **kwargs)

    # Ajout des champs propres à Profile dans un composé Inline
    def change_view(self, *args, **kwargs):
      self.inlines = (ProfilInline,)
      return super(CustomUserAdmin, self).change_view(*args, **kwargs)

    # Tout utilisateur est considéré comme staff par défaut (ie ayant accès à l'interface d'administration),
    # puisque c'est la seule raison d'enregistrer les utilisateurs dans notre projet.
    def save_model(self, request, obj, form, change):
        obj.is_staff = True
        super(CustomUserAdmin, self).save_model(request, obj, form, change)

    # Annule le comportement par défaut du bouton Save qui renvoie vers CustomUserChangeForm
    def response_add(self, request, obj, post_url_continue=None):
        return super(UserAdmin, self).response_add(request, obj, post_url_continue)

# Annule l'enregistrement de l'interface admin par défaut de gestion des utilisateurs
# et remplace par la nôtre (définie ci-dessus)
try:
    admin.site.unregister(User)
except NotRegistered:
    pass
admin.site.register(User, CustomUserAdmin)
