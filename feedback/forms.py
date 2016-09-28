from django import forms
from feedback.models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        widgets = {
          'description': forms.Textarea(attrs={'rows':2,}),
          'suggestion': forms.Textarea(attrs={'rows':2,}),
#          'type': forms.RadioSelect(),
        }
        exclude = []
