from django import forms
from gestion.models import AprobacionPA

class FormularioAprobacionPA(forms.ModelForm):
    class Meta:
        model = AprobacionPA
        fields = ('tipo', 'comentario')
        widgets = {
          'comentario': forms.Textarea(attrs={'rows':3}),
        }