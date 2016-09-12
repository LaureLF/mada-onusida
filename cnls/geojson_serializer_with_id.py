from django.contrib.gis.serializers.geojson import Serializer as GeojsonSerializer

# Personnalisation de la création des GeoJson
class GeojsonWithIdSerializer(GeojsonSerializer):
        
    def get_dump_object(self, obj):
        # Inclure le champ id (pas présent par défaut)
        self._current['id']=obj.pk
        # Inclure le nom de la classe de l'objet
        self._current['classe']= obj.__class__.__name__
        # Exclure un certain nombre de champs inutiles
        fields_to_remove = {'objectif', 'date_debut', 'date_fin', 'duree', 'createur', 'commentaire', 'montant_prevu', 'montant_disponible', 'devise', 'origine', 'contact', 'operateur', 'resultat_cf_annee_ant', 'priorite_psn', 'creation', 'maj', 'login_maj', 'validation'}
        for key in fields_to_remove:
            if key in self._current:
                del self._current[key]
        return GeojsonSerializer.get_dump_object(self, obj)
