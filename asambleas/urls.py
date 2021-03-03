from django.urls import path
from . import views

app_name = "asambleas"

urlpatterns = [
    path('', views.principal, name="principal"),
    path('lista_secciones_propuesta', views.ListaSeccionesPropuesta.as_view(), name='lista_secciones_propuesta'),
    path('crear_seccion_propuesta', views.CrearSeccionPropuesta.as_view(), name='crear_seccion_propuesta'),
    path('ver_propuesta_asamblea', views.VerPropuestaAsamblea.as_view(), name='ver_propuesta_asamblea'),
    path('crear_seccion_individual', views.CrearSeccionIndividual.as_view(), name='crear_seccion_individual'),
    path('lista_secciones_individuales', views.ListaSeccionesIndividuales.as_view(), name='lista_secciones_individuales'),
    path('ver_secciones_individuales_de_asamblea', views.VerSeccionesIndividuales.as_view(), name='ver_secciones_individuales_de_asamblea'),
]