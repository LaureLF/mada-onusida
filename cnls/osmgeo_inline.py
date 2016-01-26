from django.forms.models import ModelForm
from django.contrib.admin.options import TabularInline
from django.contrib import admin
from django.contrib.gis.forms.fields import GeometryField

class OSMGeoInlineForm(ModelForm):
    """
    A form to go along with the OSMGeoTabularInline to set GeometryField's widgets to the correct map widget
    
    A subclass can set a params option, a dict that will override the map widget's params. The keys of the dict are the names of the map options to override.
    eg. params = {'map_width': 300, 'map_height': 300, 'default_zoom': 10}
    see GeoModelAdmin for the available options.
    """
    def __init__(self, *args, **kwargs):
        super(OSMGeoInlineForm, self).__init__(*args, **kwargs)
        model_admin_instance = admin.sites.site._registry[self.parent_model]
        
        for field in self.fields:
            if isinstance(self.fields[field], GeometryField):
                model_field = self._meta.model._meta.get_field(field)
                self.fields[field].widget = model_admin_instance.get_map_widget(model_field)()
                if hasattr(self, 'params'):
                    for param in self.params:
                        self.fields[field].widget.params[param] = self.params[param]
        
    class Media:
        js = ('jquery.rule-1.0.1.1-min.js',) # Change this if you store the jquery rule file elsewhere

class OSMGeoTabularInline(TabularInline):
    """
    A subclass of TabularInline that allows OSMGeoAdmin map widgets to be used for GeometryFields
    
    You must subclass this just the same as TabularInline and provide the model option
    You can also set a params option, a dict that will be passed to OSMGeoInlineForm to override the map widgets params. See OSMGeoInlineForm for details.
    """
    template = 'admin/osmgeo_tabular_inline.html'
    form = OSMGeoInlineForm
    
    def __init__(self, parent_model, admin_site):
        self.form.parent_model = parent_model
        if hasattr(self, 'params'):
            self.form.params = self.params
        super(OSMGeoTabularInline, self).__init__(parent_model, admin_site)