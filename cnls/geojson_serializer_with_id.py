from django.contrib.gis.serializers.geojson import Serializer as GeojsonSerializer

class GeojsonWithIdSerializer(GeojsonSerializer):
        
    def get_dump_object(self, obj):
        self._current['id']=obj.pk
        self._current['classe']= obj.__class__.__name__
        fields_to_remove = {'objectif', 'date_debut', 'date_fin', 'duree', 'createur', 'commentaire', 'montant_prevu', 'montant_disponible', 'devise', 'origine', 'contact', 'operateur', 'resultat_cf_annee_ant', 'priorite_psn', 'creation', 'maj', 'login_maj'}
        for key in fields_to_remove:
            if key in self._current:
                del self._current[key]
        return GeojsonSerializer.get_dump_object(self, obj)
