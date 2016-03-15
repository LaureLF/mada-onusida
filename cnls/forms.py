from django import forms
from django.contrib.gis.geos import Point, MultiPoint
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
import re
from cnls.models import Action

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

class CustomUserChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


#reg = re.compile(r'^\s*\(\s*(-?\s*\d+(?:\.\d+)?)\s*,\s*(-?\s*\d+(?:\.\d+)?)\s*\)\s*$')
regex = r'^\s*(-?\s*\d+(?:\.\d+)?)\s*,\s*(-?\s*\d+(?:\.\d+)?)\s*$'
       
class CustomAdminForm(forms.ModelForm):

    def validate_multipoint(value):
        for line in value.splitlines():
            match = re.match(regex, line)
            if not match:
                raise ValidationError('(%(line)s) n\'est pas au format attendu.', params={'line': line}, code='invalid')
            lat = float(match.group(1).replace(" ",""))
            lon = float(match.group(2).replace(" ",""))
            if not (-26<lat<-11 and 42<lon<52):
                raise ValidationError('Le point %(line)s n\'est pas situé à Madagascar.', params={'line': line}, code='invalid')

    mpoint_text = forms.CharField(label = 'Coordonnées GPS', help_text = "Veuillez renseigner les coordonnées ligne par ligne, sous la forme : latitude, longitude", required = False, widget = forms.Textarea, validators=[validate_multipoint])  
    #choix srid?
   
    def clean(self):
        #run the standard clean method first
        cleaned_data = super(CustomAdminForm, self).clean()  
        # validations sur la géométrie   
        mpoint_text = cleaned_data.get("mpoint_text")
        mpoint = cleaned_data.get("mpoint")

        if (not mpoint) and (not mpoint_text):
            self.add_error('mpoint', ValidationError("Veuillez renseigner au moins une localisation (carte ou coordonnées GPS).", code='invalid'))
        if mpoint and mpoint_text:
            self.add_error('mpoint', ValidationError("Pour éviter les doublons, merci de renseigner uniquement la carte OU les coordonnées.", code='invalid'))
        if mpoint_text:
            points = []
            for line in mpoint_text.splitlines():
                match = re.match(regex, line)
                lat = float(match.group(1).replace(" ",""))
                lon = float(match.group(2).replace(" ",""))
                points.append(Point(lon, lat, srid=4326))
            # on envoie le MultiPoint créé sur le champ mpoint
            cleaned_data['mpoint'] = MultiPoint(points)           

        # validation sur la devise si on rentre un montant
        montant_prevu = cleaned_data.get("montant_prevu")
        montant_disponible = cleaned_data.get("montant_disponible")
        devise = cleaned_data.get("devise")
        if (montant_prevu or montant_disponible) and not devise:
            self.add_error('devise', ValidationError("Veuillez préciser la devise des fonds.", code='invalid'))
        return cleaned_data
        
    class Meta:
        model = Action
        exclude = []
 