from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic import DetailView, DeleteView
from django.views.generic.base import View
from gestion.models import Seccion, SeccionIndividual, PropuestaAsamblea, Asamblea

from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.

def principal(request):
    return render(request, 'asambleas/principal.html')


# CRUD Secciones Propuesta Asamblea

# Mixins
from django.contrib.messages.views import SuccessMessageMixin

# the final action completed by this mixin may be done with instructions
# placed inside get_success_url() method overriding it.
class BorrarVotacionesMixin:

    def form_valid(self, form):
        # The super call to form_valid creates a model instance
        # under self.object.
        response = super().form_valid(form)
        # Borrar todas las votaciones previas
        AprobacionPA.objects.all().delete()
        return response

# C de CRUD
class CrearSeccionPropuesta(SuccessMessageMixin, BorrarVotacionesMixin, CreateView):
    model = Seccion
    fields = ['titulo', 'texto', 'tema']
    template_name = 'asambleas/crear_seccion.html'
    success_url = reverse_lazy('asambleas:lista_secciones_propuesta')
    success_message = 'APROBACIONES BORRADAS: Debe solicitar aprobaciones nuevamente!'

    def form_valid(self, form):
        form.instance.propuesta_asamblea = self.request.user.asamblea.propuestaasamblea
        return super(CrearSeccionPropuesta, self).form_valid(form)


# R de CRUD
class ListaSeccionesPropuesta(ListView):
    model = Seccion
    template_name = 'asambleas/secciones.html'
    context_object_name = 'secciones'

    def get_queryset(self):
        return Seccion.objects.filter(propuesta_asamblea=self.request.user.asamblea.propuestaasamblea).order_by('id')


# U de CRUD
class EditarSeccionPropuesta(SuccessMessageMixin, BorrarVotacionesMixin, UpdateView):
    model = Seccion
    template_name = 'asambleas/editar_seccion.html'
    fields = ['titulo','texto','tema']
    success_url = reverse_lazy('asambleas:lista_secciones_propuesta')
    success_message = 'APROBACIONES BORRADAS: Debe solicitar aprobaciones nuevamente!'


# D de CRUD
class EliminarSeccionPropuesta(SuccessMessageMixin, BorrarVotacionesMixin, DeleteView):
    model = Seccion
    context_object_name = 'seccion'
    template_name = 'asambleas/eliminar_seccion.html'
    success_url = reverse_lazy('asambleas:lista_secciones_propuesta')
    success_message = 'APROBACIONES BORRADAS: Debe solicitar aprobaciones nuevamente!'


# CRUD Secciones Individuales


# C de CRUD
class CrearSeccionIndividual(CreateView):
    model = SeccionIndividual
    fields = ['titulo', 'texto', 'tema']
    template_name = 'asambleas/crear_seccion_individual.html'
    success_message = 'APROBACIONES BORRADAS: Debe solicitar aprobaciones nuevamente!'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearSeccionIndividual, self).form_valid(form)


# R de CRUD
class ListaSeccionesIndividuales( ListView):
    model = SeccionIndividual
    template_name = 'asambleas/lista_secciones_individuales.html'
    context_object_name = 'secciones'

    def get_queryset(self):
        return SeccionIndividual.objects.filter(usuario=self.request.user).order_by('id')


# U de CRUD

# D de CRUD



from .forms import FormularioAprobacionPA
from gestion.models import AprobacionPA
# Ver Propuesta Asamblea
class VerPropuestaAsamblea(ListView):
    model = Seccion
    template_name = 'asambleas/ver_propuesta_asamblea.html'
    context_object_name = 'secciones'
    form_class = FormularioAprobacionPA
    model_aprobacion = AprobacionPA

    def get_queryset(self):
        return Seccion.objects.filter(propuesta_asamblea=self.request.user.asamblea.propuestaasamblea).order_by('id')

    def get_context_data(self, **kwargs):
        context = super(VerPropuestaAsamblea, self).get_context_data(**kwargs) # default
        context['asamblea'] = self.request.user.asamblea # objeto extra
        context['form'] = self.form_class
        context['num_aprobaciones'] = len(self.model_aprobacion.objects.filter(tipo=1))
        context['num_rechazos'] = len(self.model_aprobacion.objects.filter(tipo=2))
        if len(self.model_aprobacion.objects.filter(usuario=self.request.user))==0:
            context['mostrar_voto'] = True
        else:
            context['mostrar_voto'] = False
            context['voto'] = self.model_aprobacion.objects.get(usuario=self.request.user).get_tipo_display()

        return context
    
    def post(self, request):
        formulario = self.form_class(request.POST)
        if formulario.is_valid():
            form_data = formulario.cleaned_data
            self.model_aprobacion.objects.create(
                            tipo = form_data['tipo'],
                            comentario = form_data['comentario'],
                            usuario = self.request.user,
                            propuesta_asamblea = request.user.asamblea.propuestaasamblea
                            )
            return redirect('asambleas:ver_propuesta_asamblea')
        context = {self.context_object_name:self.get_queryset()}
        context['asamblea'] = self.request.user.asamblea
        context['form'] = formulario
        if len(self.model_aprobacion.objects.filter(usuario=self.request.user))==0:
            context['mostrar_voto'] = True
        else:
            context['mostrar_voto'] = False
            context['voto'] = self.model_aprobacion.objects.get(usuario=self.request.user).get_tipo_display()
        #self.object_list = self.get_queryset()
        return render(self.request, self.template_name, context)



# Ver Secciones Individuales de la Asamblea
class VerSeccionesIndividuales(ListView):
    model = SeccionIndividual
    template_name = 'asambleas/ver_secciones_individuales_de_asamblea.html'
    context_object_name = 'secciones'

    def get_queryset(self):
        asamblea = self.request.user.asamblea
        usuarios_asamblea = asamblea.usuario_set.all()
        print(usuarios_asamblea)
        return SeccionIndividual.objects.filter(usuario__in=usuarios_asamblea).order_by('id')


# CRUD Asambleas para Administrador

# C de CRUD
class CrearAsamblea(CreateView):
    model = Asamblea
    fields = ['nombre','descripcion','telefono','email','direccion_calle','direccion_numero','comuna']
    template_name = 'asambleas/crear_asamblea.html'
    success_url = reverse_lazy('asambleas:lista_asambleas')

    # Se crea la propuesta asamblea en este método para tener acceso a objeto creado, luego de haber sido guardado
    # Si se hace en form_valid() el id no se puede acceder pues aún no lo asigna la base de datos
    def get_success_url(self):
        PropuestaAsamblea.objects.create(
                        titulo="Propuesta de Asamblea "+self.object.nombre,
                        descripcion = "Descripción de "+self.object.nombre,
                        asamblea=self.object,
                        usuario_actualizacion=self.request.user
        )
        return self.success_url


# R de CRUD
class ListaAsambleas(ListView):
    model = Asamblea
    template_name = 'asambleas/lista_asambleas.html'
    context_object_name = 'asambleas'


from .forms import EditarAsambleaForm
# U de CRUD
class EditarAsamblea(UpdateView):
    model = Asamblea
    form_class = EditarAsambleaForm
    template_name = 'asambleas/editar_asamblea.html'
    #fields = ['nombre','descripcion','telefono','email','direccion_calle','direccion_numero','comuna']
    success_url = reverse_lazy('asambleas:lista_asambleas')
    
    def form_valid(self, form):
        form.instance.representante = form.cleaned_data['representante']
        print(User.objects.get(id=int(form.instance.representante)))
        ### AQUI FALTA GUARDAR EL REPRESENTANTE Y CAMBIAR A MIEMBRO EL REPRESENTANTE ANTERIOR
        return super(EditarAsamblea, self).form_valid(form)



# D de CRUD

