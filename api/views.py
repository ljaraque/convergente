# api/views.py
from rest_framework import viewsets
from gestion.models import Usuario
from api.serializers import UsuarioSerializer

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
