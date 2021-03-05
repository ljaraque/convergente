from django import forms
from django.contrib.auth import get_user_model
from gestion.models import AprobacionPA, Asamblea

User=get_user_model()

class FormularioAprobacionPA(forms.ModelForm):
    class Meta:
        model = AprobacionPA
        fields = ('tipo', 'comentario')
        widgets = {
          'comentario': forms.Textarea(attrs={'rows':3}),
        }


class EditarAsambleaForm(forms.ModelForm):
  
  #representante = forms.ChoiceField(choices=[
  #  (choice.pk, choice) for choice in User.objects.all()])

  class Meta:
    model=Asamblea
    fields='__all__'

  def __init__(self, *args, **kwargs):
      #asamblea_id = kwargs.pop("asamblea_id")
      asamblea = kwargs['instance']
      print(asamblea.id)
      super(EditarAsambleaForm, self).__init__(*args, **kwargs)
      self.fields['representante']= forms.ChoiceField(choices=[
              (choice.pk, choice) for choice in User.objects.filter(asamblea=asamblea)])
