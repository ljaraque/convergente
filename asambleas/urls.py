from django.urls import path
from . import views

app_name = "asambleas"

urlpatterns = [
    path('', views.principal, name="principal"),
    path('lista_secciones_propuesta', views.ListaSeccionesPropuesta.as_view(), name='lista_secciones_propuesta'),
    path('crear_seccion_propuesta', views.CrearSeccionPropuesta.as_view(), name='crear_seccion_propuesta'),
    path('<pk>/editar_seccion_propuesta', views.EditarSeccionPropuesta.as_view(), name='editar_seccion_propuesta'),
    path('<pk>/eliminar_seccion_propuesta', views.EliminarSeccionPropuesta.as_view(), name='eliminar_seccion_propuesta'),
    path('ver_propuesta_asamblea', views.VerPropuestaAsamblea.as_view(), name='ver_propuesta_asamblea'),
    path('crear_seccion_individual', views.CrearSeccionIndividual.as_view(), name='crear_seccion_individual'),
    path('lista_secciones_individuales', views.ListaSeccionesIndividuales.as_view(), name='lista_secciones_individuales'),
    path('ver_secciones_individuales_de_asamblea', views.VerSeccionesIndividuales.as_view(), name='ver_secciones_individuales_de_asamblea'),
    path('lista_asambleas', views.ListaAsambleas.as_view(), name='lista_asambleas'),
    path('crear_asamblea', views.CrearAsamblea.as_view(), name='crear_asamblea'),
    path('<pk>/editar_asamblea', views.EditarAsamblea.as_view(), name='editar_asamblea'),
    path('voto_toggle/', views.voto_toggle, name='voto_toggle'),
    path('lista_usuarios/', views.ListaUsuarios.as_view(), name='lista_usuarios'),
]