# api/views.py
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from gestion.models import Usuario
from api.serializers import UsuarioSerializer
from gestion.models import Asamblea
from .serializers import AsambleaSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class AsambleaListView(generics.ListAPIView):
    queryset = Asamblea.objects.all()
    serializer_class = AsambleaSerializer
    permission_classes = (IsAuthenticated,)