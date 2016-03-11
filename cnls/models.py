#-*- coding: utf-8 -*-
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
from django.utils.timezone import now
#from django.db.models.signals import post_save

"""
# Create your models here.
# Les "Primary Key" de chaque classe sont générées automatiquement (champs id)
"""

# FARITRA
class Faritra(models.Model):
    # Décret n°2015 – 593 du 1er avril 2015 on www.mid.gov.mg
    FARITRA = (
    ('Antananarivo', (
#      ("anta-pref", "Préfecture de Police d'Antananarivo"),      
      ("anta-anal", "Analamanga"),
      ("anta-tsir", "Tsiroanomandidy"),
      ("anta-miar", "Miarinarivo"),
      ("anta-ants", "Antsirabe"),
    )),
    ('TOAMASINA', (
      ("toam-toam", "Toamasina"),
      ("toam-amba", "Ambatondrazaka"),
      ("toam-fene", "Fénérive Est"),
      ("toma-pref", "Préfecture de police de Sainte Marie"),
    )),
    ('ANTSIRANANA', (
      ("ants-ants", "Antsiranana"),
      ("ants-samb", "Sambava"),
      ("ants-nosy", "Préfecture de police de Nosy Be"),
    )),
    ('FIANARANTSOA', (
      ("fian-fian", "Fianarantsoa"),
      ("fian-ambo", "Ambositra"),
      ("fian-mana", "Manakara"),
      ("fian-fara", "Farafangana"),
      ("fian-ihos", "Ihosy"),      
    )),
    ('MAHAJANGA', (
      ("maha-maha", "Mahajanga"),
      ("maha-maev", "Maevatanana"),
      ("maha-ants", "Antsohihy"),
      ("maha-main", "Maintirano"),    
    )),
    ('TOLIARY', (
      ("toli-toli", "Toliary"),
      ("toli-ambo", "Ambovombe"),
      ("toli-taol", "Taolagnaro"),
      ("toli-moro", "Morondava"),     
    )),
    )
    nom = models.CharField(max_length=50, choices=FARITRA)
#    nom = models.CharField(max_length=50, verbose_name=u"Nom de la région", default='')
#    mpoint = models.PointField(default='SRID=4326;POINT(0.0 0.0)', verbose_name="Coordonnées de la capitale de région")
#    objects = models.GeoManager()
   
    class Meta:
        verbose_name = "Préfecture - Faritra"
        verbose_name_plural = "Préfectures - Faritra"

    def __str__(self):
        return self.get_nom_display()

    def natural_key(self):
        return (self.get_nom_display(),)



# FOKONTANY
class Fokontany(models.Model):
    FOKONTANY = (
    ('tana1', 'Tana I - Analakely'),
    ('tana2', 'Tana II - Ambanidia'),
    ('tana3', 'Tana III - Antaninandro'),
    ('tana4', 'Tana IV - Mahamasina'),
    ('tana5', 'Tana V - Ambatomainty'),
    ('tana6', 'Tana VI - Ambohimanarina'),
    )
    nom = models.CharField(max_length=50, choices=FOKONTANY)
#    nom = models.CharField(max_length=50, verbose_name=u"Nom du fokontany", default='') 
#    mpoint = models.PointField(default='SRID=4326;POINT(0.0 0.0)', verbose_name="Coordonnées du fokontany")
#    objects = models.GeoManager()
    class Meta:
        verbose_name = "Arrondissement - Fokontany"
        verbose_name_plural = "Arrondissements - Fokontany"

    def __str__(self):
        return self.get_nom_display()

    def natural_key(self):
        return (self.get_nom_display(),)


# KAOMININA
class Kaominina(models.Model):
    KAOMININA = (
    # from external file??
    ('commune1', 'Commune1'),
    ('commune2', 'Commune2'),
    ('commune3', 'Commune3'),
    ('commune4', 'Commune4'),
    )
    nom = models.CharField(max_length=50, choices=KAOMININA)
#    nom = models.CharField(max_length=50, verbose_name=u"Nom de la commune", default='') 
#    mpoint = models.PointField(default='SRID=4326;POINT(0.0 0.0)', verbose_name="Coordonnées de la commmune")
#    objects = models.GeoManager()
    class Meta:
        verbose_name = "Commune - Kaominina"
        verbose_name_plural = "Communes - Kaominina"
    def __str__(self):
        return self.get_nom_display()
    def natural_key(self):
        return (self.get_nom_display(),)
        
        
#########################################
# CIBLE
class Cible(models.Model):
    LISTE= (
        ('1-pg', u'Population générale'),
        ('Adultes', (
          ('2-pvalv', u'Personnes vivant avec le VIH'),
          ('2-pdv', u'Perdus de vue'),
          ('2-cddi', u'Consommateurs de drogues injectables'),
          ('2-hadradah', u'Homme ayant des rapports avec d’autres hommes'),
          ('2-tds', u'Travailleuses du sexe'),
          ('2-hacahr', u'Hommes à comportements à hauts risques'),
          ('2-cdtds', u'Clients des travailleuses du sexe'),
          ('2-pm', u'Populations migrantes'),
          ('2-pc', u'Population carcérale'),
          ('2-fa', u'Forces armées'),
          ('2-fe', u'Femmes enceintes'),
          ('2-fvdvs', u'Femmes victimes de violences sexuelles'),
          ('2-lrot', u'Leaders religieux ou traditionnels'),
          ('2-pds', u'Personnels de santé'),
          ('3-a', u'Autres (Cercles associatifs, cercles religieux, etc)'),
          )),
        ('Jeunes', (
          ('5-js', u'Jeunes scolarisés'),
          ('5-jns', u'Jeunes non-scolarisés'),
          ('5-oeev', u'Orphelins et enfants vulnérables'),
          )),
    )

    nom = models.CharField(max_length=80, choices=LISTE)
    
    class Meta:
        managed = True
        verbose_name = "Cible"
        verbose_name_plural = "Cibles"
        ordering = ['nom']

    def natural_key(self):
        return (self.get_nom_display(),)
   
    def __str__(self):
        return self.get_nom_display()


# TYPE D'INTERVENTION
class TypeIntervention(models.Model):
    TYPE= (
        (u'plaidoyer', u'Plaidoyer'),
        (u'ccc', u'CCC'),
        (u'preservatifs', u'Promotion de préservatifs'),
        (u'communication', u'Communication de masse'),
        (u'ist', u'Prise en charge IST'),
        (u'medical', u'Prise en charge médicale'),
        (u'soutien', u'Soutien'),
        (u'coordination', u'Coordination'),
        (u'renforcement', u'Renforcement de capacités'),
        (u'depistage', u'Dépistage'),
    )

    nom = models.CharField(max_length=40, choices=TYPE)
    descriptif = models.TextField(blank=True, default='', verbose_name="Description du type d'intervention")
#    picto ?

    class Meta:
        managed = True
        ordering = ['nom']
        verbose_name = "Type d'intervention"
        verbose_name_plural = "Types d'intervention"

    def __str__(self):
        return self.get_nom_display()

    def natural_key(self):
        return (self.get_nom_display(),)

#################################
# ORGANISME
class Organisme(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, default='')
    logo = models.ImageField(upload_to="static/media/logo/", blank=True, default="static/media/logo/defaultLogo.png")
    referent = models.ForeignKey('self', blank=True, null=True)
    
    def natural_key(self):
        return (self.nom,)

    class Meta:
        managed = True
        verbose_name = 'Organisme'
        verbose_name_plural = "Organismes"
        ordering = ['nom']

    def __str__(self):
        return self.nom

# PROFIL
class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organisme = models.ForeignKey(Organisme, verbose_name="Organisme / Structure", null = True)
    poste = models.CharField(max_length = 250, verbose_name="Poste ou responsabilité occupé(e)", null=True, blank = True)
    photo = models.ImageField(blank=True, upload_to="static/media/photos/", default="static/media/photos/defaultPicture.png")
 
    def natural_key(self):
        return (self.user.username, self.user.first_name, self.user.last_name,)

    class Meta:
        managed = True
        verbose_name = "Profil"
        verbose_name_plural = "Profils"
#        ordering = ['user']

    def __str__(self):
#        return u"User: %s" % self.user.username
        return self.user.username

#    def appartenance(self):
#        "Returns the Organisme and person's full name."
#        return u"%s %s : %s" % (self.first_name, self.last_name, self.Organisme)
#    appartenance.allow_tags = True
#    affiliation = property(appartenance)

#####################################
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
    TANANARIVE = Point(-18.933333, 47.516667, srid=4326)
    NATIONALE = Point(-19.647189, 43.881133, srid=4326)
    
    titre = models.CharField(max_length = 250, verbose_name="Titre de l'action", help_text="Donnez un titre court et explicite. Pour plus d'informations, utilisez le champ suivant (description).")
    organisme = models.ForeignKey(Organisme, verbose_name="Organisme maître d'œuvre")
    typeintervention = models.ManyToManyField(TypeIntervention, verbose_name="Types d'interventions")
    cible = models.ManyToManyField(Cible, verbose_name="Publics cibles")
    objectif = models.PositiveIntegerField(null=True, blank=True, verbose_name="Nombre de personnes visées")
    
    date_debut = models.DateField("Date de démarrage", auto_now_add=False, auto_now=False)
    date_fin = models.DateField("Date de fin", auto_now_add=False, auto_now=False)
    duree = models.CharField(max_length=40, blank=True, default='', verbose_name="Durée de l'action") 
    avancement = models.CharField( max_length=10,choices=AVANCEMENT, default='en cours',verbose_name="État d'avancement") 

    createur = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_related", verbose_name="Nom du responsable de la fiche")
    description = models.TextField(blank=True, default='', verbose_name="Description de l'action")
    commentaire = models.TextField(blank=True, default='', verbose_name="Observations ou commentaires")

    montant_prevu = models.PositiveIntegerField(null=True, blank=True, verbose_name="Montant prévu")
    montant_disponible = models.PositiveIntegerField(null=True, blank=True, verbose_name="Montant disponible")
    devise = models.CharField(max_length=10,choices=DEVISE, default='EUR')
    bailleurfond = models.CharField(max_length = 100, blank=True, verbose_name="Bailleurs de fond", default='')
    origine = models.CharField(max_length = 100,verbose_name="Origine de la donnée", blank=True, default='')
    contact = models.EmailField(max_length = 100, verbose_name="Adresse email de contact")
    
    operateur = models.CharField(max_length = 100, blank=True, verbose_name="Opérateur en lien avec l'action", default='')
    resultat_cf_annee_ant = models.CharField(max_length = 250, blank=True, verbose_name="Résultat par rapport à l'année précédente", default='')
    priorite_psn = models.CharField(max_length = 100, blank=True, verbose_name="Priorité du PSN que l'activité appuie", default='')

    mpoint = models.MultiPointField(default='SRID=4326;MULTIPOINT EMPTY', geography=True, srid=4326, verbose_name="Coordonnées géographiques", help_text="Détermine la position de l'action sur la carte.", blank=True)
    objects = models.GeoManager()
 
    creation = models.DateTimeField("Date de création fiche")
    maj = models.DateTimeField("Date de la dernière mise à jour fiche")
    login_maj = models.ForeignKey(User, related_name="%(app_label)s_%(class)s_maj_related", verbose_name="Utilisateur responsable de la dernière mise à jour")

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

# TODO
    # Controle de l'ancienneté de la fiche
    #def control_obsolescence(self):atlas
    #    "Returns Action's obsolescence record Status."
    #Vérifier si le Status actuel d'Avancement n'est pas "Terminé" et que la date de "maj" est supérieur à 1 an..

# ActionNationale
class ActionNationale(Action):
    class Meta:
        verbose_name = "'Action au niveau national'"
        verbose_name_plural = "   Actions au niveau national"

# ActionTananarive
class ActionTananarive(Action):
    fokontany = models.ManyToManyField(Fokontany, verbose_name="Fokontany(s)")
    class Meta:
        verbose_name = "'Action dans la capitale'"
        verbose_name_plural = "  Actions dans la capitale"

# ActionRegionale
class ActionRegionale(Action):
    region = models.ManyToManyField(Faritra, verbose_name="Régions")
    class Meta:
        verbose_name = "'Action au niveau de la préfecture (faritra)'"
        verbose_name_plural = " Actions au niveau de la préfecture (faritra)"

# ActionLocale
class ActionLocale(Action):
    commune = models.ManyToManyField(Kaominina, verbose_name="Communes")
    class Meta:
        verbose_name = "'Action au niveau communal'"
        verbose_name_plural = "Actions au niveau communal"