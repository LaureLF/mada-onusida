from django import forms
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.gis.geos import Point, MultiPoint
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import re
from cnls.models import Action, Organisme, Profil

####################
# Modification du formulaire par défaut pour la création et la modification d'utilisateurs
####################
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        # Ces champs seront obligatoires (ce n'est pas le cas par défaut pour le modèle User)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    # Personnalisation du choix du groupe
    groups = forms.ModelChoiceField(queryset=Group.objects.all().order_by('-name'), widget=forms.RadioSelect, empty_label=None, initial=1)
    # Champs supplémentaires du modèle Profil
    organisme = forms.ModelChoiceField(queryset=Organisme.objects.all(), to_field_name="nom")
    poste = forms.CharField(max_length=250, required=True)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        exclude = []

    # On enregistre le modèle User avec la procédure par défaut, et à part les champs du modèle Profil
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=True)
        user_profile = Profil(user=user, organisme=self.cleaned_data['organisme'], poste=self.cleaned_data['poste'], photo=self.cleaned_data['photo'])
        user_profile.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


####################
####################
# Expression régulière pour récupérer latitudes et longitudes entrées par l'utilisateur
#reg = re.compile(r'^\s*\(\s*(-?\s*\d+(?:\.\d+)?)\s*,\s*(-?\s*\d+(?:\.\d+)?)\s*\)\s*$')
regex = r'^\s*(-?\s*\d+(?:\.\d+)?)\s*,\s*(-?\s*\d+(?:\.\d+)?)\s*$'

class CustomAdminForm(forms.ModelForm):
    def validate_multipoint(value):
        for line in value.splitlines():
            # Les coordonnées sont attendues une par ligne, sous la forme : latitude, longitude
            # comme spécifié dans le help_text du champ mpoint_text
            match = re.match(regex, line)
            if not match:
                raise ValidationError('(%(line)s) n\'est pas au format attendu.', params={'line': line}, code='invalid')
            lat = float(match.group(1).replace(" ",""))
            lon = float(match.group(2).replace(" ",""))
            # Test très grossier pour vérifier qu'il n'y a pas eu d'inversion entre latitude et longitude
            if not (-26<lat<-11 and 42<lon<52):
                raise ValidationError('Le point %(line)s n\'est pas situé à Madagascar.', params={'line': line}, code='invalid')

    mpoint_text = forms.CharField(label = 'Coordonnées GPS', help_text = "Veuillez renseigner les coordonnées ligne par ligne, sous la forme : latitude, longitude", required = False, widget = forms.Textarea, validators=[validate_multipoint])  
    # TODO choix srid?

    def clean(self):
        # D'abord la méthode par défaut
        cleaned_data = super(CustomAdminForm, self).clean()
        # puis on récupère le contenu de certains champs pour faire des validations particulières
        mpoint_text = cleaned_data.get("mpoint_text")
        mpoint = cleaned_data.get("mpoint")
        # S'assurer qu'au moins une localisation a été fournie
        if (not mpoint) and (not mpoint_text):
            self.add_error('mpoint', ValidationError("Veuillez renseigner au moins une localisation (carte ou coordonnées GPS).", code='invalid'))
        # S'assurer qu'il n'y ait pas des données et sur la carte et dans le champ texte pour éviter les doublons
        if mpoint and mpoint_text:
            self.add_error('mpoint', ValidationError("Pour éviter les doublons, merci de renseigner uniquement la carte OU les coordonnées.", code='invalid'))
        if mpoint_text:
            points = []
            # On récupère les coordonnées remplies à la main pour en faire un une géométrie
            for line in mpoint_text.splitlines():
                match = re.match(regex, line)
                lat = float(match.group(1).replace(" ",""))
                lon = float(match.group(2).replace(" ",""))
                points.append(Point(lon, lat, srid=4326))
            # on envoie le MultiPoint créé sur le champ mpoint
            cleaned_data['mpoint'] = MultiPoint(points)

        # S'assurer qu'une devise a été choisie si un montant a été rentré
        montant_prevu = cleaned_data.get("montant_prevu")
        montant_disponible = cleaned_data.get("montant_disponible")
        devise = cleaned_data.get("devise")
        if (montant_prevu or montant_disponible) and not devise:
            self.add_error('devise', ValidationError("Veuillez préciser la devise des fonds.", code='invalid'))
        # On retourne le contenu des champs pour enregistrement par Django
        return cleaned_data

    class Meta:
        model = Action
        exclude = []

