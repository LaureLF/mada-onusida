#-*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.gis.geos import GEOSGeometry, MultiPoint as GEOSMultiPoint, Point as GEOSPoint
from django.contrib.auth.models import User
from django.utils.timezone import now

"""
# Create your models here.
# Les "Primary Key" de chaque classe sont générées automatiquement (champs id)
"""

# REGION
class Region(models.Model):
    nom = models.CharField(max_length=50, verbose_name=u"Nom de la région", default='')
    mpoint = models.PointField(default='SRID=4326;POINT(0.0 0.0)', verbose_name="Coordonnées de la capitale de région")
#    mpoint = models.PointField(null=True, verbose_name=u"Coordonnées de la capitale de région")
    objects = models.GeoManager()
   
    class Meta:
        verbose_name = "Région"
        verbose_name_plural = "Régions"

    def __str__(self):
        return self.nom

    def natural_key(self):
#        return (self.mpoint.coords,)
        return (self.nom,)


# COMMUNE
class Commune(models.Model):
    nom = models.CharField(max_length=50, verbose_name=u"Nom de la commune", default='') 
    mpoint = models.PointField(default='SRID=4326;POINT(0.0 0.0)', verbose_name="Coordonnées de la commmune")
#    mpoint = models.PointField(null=True, verbose_name=u"Coordonnées de la commmune")
    objects = models.GeoManager()
    class Meta:
        verbose_name = "Commune"
        verbose_name_plural = "Communes"
    def __str__(self):
        return self.nom


# FOKONTANY
class Fokontany(models.Model):
    nom = models.CharField(max_length=50, verbose_name=u"Nom du fokontany", default='') 
    mpoint = models.PointField(default='SRID=4326;POINT(0.0 0.0)', verbose_name="Coordonnées du fokontany")
#    mpoint = models.PointField(null=True, verbose_name=u"Coordonnées du fokontany")
    objects = models.GeoManager()
    class Meta:
        verbose_name = "Fokontany"
        verbose_name_plural = "Fokontany(s)"
    def __str__(self):
        return self.nom


# CIBLE
class Cible(models.Model):
# A transformer en CharField accessible seulement par les administrateurs 
    LISTE= (
        (u'population générale', u'Population générale'),
        (u'adultes', u'Adultes'),
        (u'personnes vivant avec le vih', u'Personnes vivant avec le VIH'),
        (u'perdus de vue', u'Perdus de vue'),
        (u'consommateurs de drogues injectables', u'Consommateurs de drogues injectables'),
        (u'homme ayant des rapports avec d’autres hommes', u'Homme ayant des rapports avec d’autres hommes'),
        (u'travailleuses du sexe', u'Travailleuses du sexe'),
        (u'hommes à comportements à hauts risques', u'Hommes à comportements à hauts risques'),
        (u'clients des tds', u'Clients des TdS'),
        (u'populations migrantes', u'Populations migrantes'),
        (u'population carcérale', u'Population carcérale'),
        (u'forces armées', u'Forces armées'),
        (u'femmes enceintes', u'Femmes enceintes'),
        (u'femmes victimes de violences sexuelles', u'Femmes victimes de violences sexuelles'),
        (u'leaders religieux ou traditionnels', u'Leaders religieux ou traditionnels'),
        (u'personnels de santé', u'Personnels de santé'),
        (u'autres (cercles associatifs, cercles religieux, etc)', u'Autres (Cercles associatifs, cercles religieux, etc)'),
        (u'jeunes', u'Jeunes'),
        (u'jeunes scolarisés', u'Jeunes scolarisés'),
        (u'jeunes non-scolarisés', u'Jeunes non-scolarisés'),
        (u'orphelins et enfants vulnérables', u'Orphelins et Enfants Vulnérables'),
    )

    nom = models.CharField(max_length=80, choices=LISTE)
    
    class Meta:
        managed = True
        verbose_name_plural = "Cibles"

    def natural_key(self):
        return (self.get_nom_display(),)
   
    def __str__(self):
        return self.get_nom_display()


# TYPE D'INTERVENTION
class Typeintervention(models.Model):
    TYPE= (
        (u'plaidoyer', u'Plaidoyer'),
        (u'ccc', u'CCC'),
        (u'promotion de préservatifs', u'Promotion de préservatifs'),
        (u'communication de masse', u'Communication de masse'),
        (u'prise en charge IST', u'Prise en charge IST'),
        (u'prise en charge médicale', u'Prise en charge médicale'),
        (u'soutien', u'Soutien'),
        (u'coordination', u'Coordination'),
        (u'renforcement de capacités', u'Renforcement de capacités'),
    )

    nom = models.CharField(max_length=40, choices=TYPE)
    descriptif = models.TextField(blank=True, default='', verbose_name="Description du type d'intervention")

    class Meta:
        managed = True
        verbose_name_plural = "Types d'intervention"

    def __str__(self):
#        return self.nom
        return self.get_nom_display()

    def natural_key(self):
        return (self.get_nom_display(),)


# ORGANISME
class Organisme(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
#    logo = models.ImageField(upload_to="static/media/logo/%Y/%m", blank=True)
    logo = models.ImageField(upload_to="static/media/logo/", blank=True, default="static/media/logo/defaultLogo.png")
#    status = models.ForeignKey('Status', verbose_name="Status", to_field='nom') # Un "Status" peut qualifier plrs "Organisme" et un "Organisme" ne peut avoir qu'un statut"  => Pas OneToOneField ni "OneToManyField" qui n'existe pas en Django mais ForeignKey## la class Status n'est pas encore défini, j'utilise donc le nom du modeleÃ  la place de l'objet model lui-mÃme
    referent = models.ForeignKey('self', blank=True, null=True)
    # TODO: is 'self' the right key?  Not clear to the user...
    
    def natural_key(self):
        return (self.nom,)

    class Meta:
        managed = True
        verbose_name = 'Organisme'
        verbose_name_plural = "Organismes"
        ordering = ['nom']

    # Retourne la chaîne de caractère définissant le modèle.
    def __str__(self):
        return self.nom

    # Retourne un court descriptif
    def short(self):
        return u"%s - %s" % (self.Status, self.nom)
    short.allow_tags = True


# UTILISATEUR   
class Utilisateur(models.Model):
    user = models.OneToOneField(User) # La liaison OneToOne vers le modèle User (mail-nom-prenom-password)
    photo = models.ImageField(blank=True, upload_to="static/media/photos/", default="static/media/photos/defaultPicture.png")
#    organisme = models.ForeignKey('Organisme') # Va servir plus tard de groupe pour inclure les "users"
    is_responsable = models.BooleanField("Responsable autorisé à éditer la fiche", default=False)
 
    def natural_key(self):
        return (self.user.username, self.user.first_name, self.user.last_name,)

    class Meta:
        managed = True
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ['user']

    def __str__(self):
#        return u"User: %s" % self.user.username
        return self.user.username

#    def appartenance(self):
#        "Returns the Organisme and person's full name."
#        return u"%s %s : %s" % (self.first_name, self.last_name, self.Organisme)
#    appartenance.allow_tags = True
#    affiliation = property(appartenance)


# ACTION
class Action(models.Model):
# TODO add help_text option to each field
    AVANCEMENT = (
   (u'en attente', u'En attente'),
   (u'en cours', u'En cours'),
   (u'termine', u'Terminé'),
    )
    DEVISE = (
    (u'MGA', u'MGA'),
    (u'EUR', u'EUR'),
    (u'USD', u'USD'),
    )

    titre = models.CharField(max_length = 250, verbose_name="Titre de l'action")
    organisme = models.ForeignKey(Organisme, verbose_name="Organisme maître d'œuvre")
    typeintervention = models.ManyToManyField(Typeintervention, verbose_name="Types d'interventions")
    cible = models.ManyToManyField(Cible, verbose_name="Publics cibles")
    objectif = models.PositiveIntegerField(null=True, blank=True, verbose_name="Nombre de personnes visées")
    
    date_debut = models.DateField("Date de démarrage", auto_now_add=False, auto_now=False)
    date_fin = models.DateField("Date de fin", auto_now_add=False, auto_now=False)
    duree = models.CharField(max_length=40, blank=True, default='', verbose_name="Durée de l'action") 
    avancement = models.CharField( max_length=10,choices=AVANCEMENT, default='en cours',verbose_name="État d'avancement") 

    createur = models.ForeignKey(Utilisateur, verbose_name="Nom du responsable de la fiche")
    description = models.TextField(blank=True, default='', verbose_name="Description de l'action")
    commentaire = models.TextField(blank=True, default='', verbose_name="Observations sur l'action")

    montant_prevu = models.PositiveIntegerField(null=True, blank=True, verbose_name="Montant prévu")
    montant_disponible = models.PositiveIntegerField(null=True, blank=True, verbose_name="Montant disponible")
    devise = models.CharField(max_length=10,choices=DEVISE, default='EUR')
    bailleurfond = models.CharField(max_length = 100, blank=True, verbose_name="Bailleurs de fond", default='')
    origine = models.CharField(max_length = 100,verbose_name="Origine de la donnée", blank=True, default='')
    contact = models.EmailField(max_length = 100,verbose_name="Mail du contact à l'origine de la donnée")
    
    operateur = models.CharField(max_length = 100, blank=True, verbose_name="Opérateur en lien avec l'action", default='')
    resultat_cf_annee_ant = models.CharField(max_length = 250, blank=True, verbose_name="Résultat par rapport à l'année précédente", default='')
    priorite_psn = models.CharField(max_length = 100, blank=True, verbose_name="Priorité du PSN que l'activité appuie", default='')

    latitude = models.DecimalField(max_digits=10, decimal_places=6, default=-18.933333, verbose_name="Latitude", null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, default=47.516667, verbose_name="Longitude", null=True, blank=True)
    mpoint = models.MultiPointField(default='SRID=4326;MULTIPOINT((0.0 0.0),(0.0 0.0))')
#    mpoint = models.PointField(null=True)
    objects = models.GeoManager()
 
    # TODO revoir la différence entre ces 3 champs
    creation = models.DateTimeField("Date de création fiche", auto_now_add=True)
    maj = models.DateTimeField("Date de la dernière mise à jour fiche", auto_now_add=True)
    # utilisateur  à la place de login_maj 
    login_maj = models.DateTimeField("Date de la dernière connection à la fiche action", auto_now_add=True)

    # Obtenir le détail des actions lors d'une requête sur les localisations
#    def natural_key(self): 
#        return (self.titre, self.avancement,) + self.organisme.natural_key() + (self.date_debut, self.date_fin, self.duree,) + self.createur.natural_key() +(self.description, self.commentaire, self.montant_prevu, self.montant_disponible, self.devise, self.bailleurfond, self.origine, self.contact, self.operateur, self.resultat_cf_annee_ant, self.priorite_psn,)

    class Meta:
        abstract = True
        managed = True
        unique_together = (('createur', 'creation',),) # nécessaire pour natural_key()
        verbose_name = "Action"
        verbose_name_plural = "Actions"
        ordering = ['-creation']
        
    def __str__(self):
        return self.titre

    # Retourne un rapide descriptif
    def short(self):
        return u"%s - %s\n%s - %s" % (self.titre, self.date.strftime("%b %d, %I:%M %p"), self.Avancement)
    short.allow_tags = True

#    def save(self, *args, **kwargs):
#        if not self.id:
#            self.creation = now()
#        self.maj = now()
#        super(Action, self).save(*args, **kwargs)

    # Controle de l'ancienneté de la fiche
    #def control_obsolescence(self):atlas
    #    "Returns Action's obsolescence record Status."
    #Vérifier si le Status actuel d'Avancement n'est pas "Terminé" et que la date de "maj" est supérieur à 1 an..

# ActionNationale
class ActionNationale(Action):
    echelle_localisation = models.CharField(max_length=10, verbose_name="Échelle de l'action", default='nationale')
#    geom = models.PointField(verbose_name=u"Coordonnées de Tananarive") # TODO ou un point dans la mer?
    class Meta:
        verbose_name = "'Action au niveau national'"
        verbose_name_plural = "   Actions au niveau national"

# ActionTananarive
class ActionTananarive(Action):
    echelle_localisation = models.CharField(max_length=10, verbose_name="Échelle de l'action", default='Tananarive') 
    fokontany = models.ManyToManyField(Fokontany, verbose_name="Fokontany(s)")
    class Meta:
        verbose_name = "'Action dans la capitale'"
        verbose_name_plural = "  Actions dans la capitale"
 
# ActionRegionale
class ActionRegionale(Action):
    echelle_localisation = models.CharField(max_length=10, verbose_name="Échelle de l'action", default='régionale') 
    region = models.ManyToManyField(Region, verbose_name="Régions")
    class Meta:
        verbose_name = "'Action au niveau régional'"
        verbose_name_plural = " Actions au niveau régional"
   
    def save(self, *args, **kwargs):
        #if (self.latitude != -18.933333 or self.longitude != 47.516667):
#        if (self.latitude != 0 or self.longitude != 0):
        # TODO ajouter contrôle grossier sur lat et lon (ici?)
        #    self.mpoint = GEOSMultiPoint(GEOSPoint((self.latitude, self.longitude)), srid=4326)
        #else:
        self.mpoint = GEOSMultiPoint([reg.mpoint for reg in self.region.all()])
        super(ActionRegionale, self).save(*args, **kwargs)  


# ActionLocale
class ActionLocale(Action):
    echelle_localisation = models.CharField(max_length=10,  verbose_name="Échelle de l'action", default='locale') 
    commune = models.ManyToManyField(Commune, verbose_name="Communes")
    class Meta:
        verbose_name = "'Action au niveau communal'"
        verbose_name_plural = "Actions au niveau communal"

"""
# Actionlocalisation
class ActionLocalisation(models.Model):
    ECHELLE_LOCALISATION = (
        (u'tananarive', u'Tananarive'),
        (u'régionale', u'Régionale'),
        (u'locale', u'Locale'),
    )
#    action = models.ForeignKey(Action)
    region_status =  models.CharField(max_length = 50, choices=ECHELLE_LOCALISATION, default='tananarive', verbose_name="Définir la localisation de l'action ?")
    choix_status = models.CharField(max_length = 50, blank=True, verbose_name="limite choisie", default='')
#L#    mpoly = models.MultiPolygonField(null=True)
#    geom = models.PointField(srid=3857,default='SRID=3857;POINT(0.0 0.0)')
    geo = models.PointField(default='SRID=4326;POINT(0.0 0.0)', verbose_name=u"Cliquez sur la localisation")
    objects = models.GeoManager()
    
    def natural_key(self):
        return self.action.natural_key()
#    natural_key.dependencies = ['cnls.Action']

    class Meta:
        managed = True
        verbose_name_plural = "Localisation"

    def __str__(self):
        return self.region_status
"""