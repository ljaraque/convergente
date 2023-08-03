# api/serializers.py
from rest_framework import serializers
from gestion.models import Usuario
from gestion.models import Asamblea

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class AsambleaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asamblea
        fields = '__all__'
