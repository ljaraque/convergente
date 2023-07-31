from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView
from django.views.generic import DetailView, DeleteView
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from gestion.models import (
    Seccion, SeccionIndividual, PropuestaAsamblea, Asamblea, Rol
)
from .forms import EditarAsambleaForm

User = get_user_model()

# funciones
def es_representante(user):
    return user.rol==Rol.objects.get(nombre="Representante")

def es_miembro(user):
    return user.rol==Rol.objects.get(nombre="Miembro")

def es_administrador(user):
    return user.rol==Rol.objects.get(nombre="Administrador")

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
class CrearSeccionPropuesta(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin,
    BorrarVotacionesMixin, CreateView
):
    
    model = Seccion
    fields = ['tema','titulo', 'texto']
    template_name = 'asambleas/crear_seccion.html'
    success_url = reverse_lazy('asambleas:lista_secciones_propuesta')
    success_message = (
        'APROBACIONES BORRADAS: '
        'Debe solicitar aprobaciones nuevamente!'
    )

    def form_valid(self, form):
        form.instance.propuesta_asamblea = (
            self.request.user.asamblea.propuestaasamblea
        )
        return super(CrearSeccionPropuesta, self).form_valid(form)

    def test_func(self):
        return es_representante(self.request.user)


# R de CRUD
class ListaSeccionesPropuesta(
    LoginRequiredMixin, UserPassesTestMixin, ListView
):
    
    model = Seccion
    template_name = 'asambleas/secciones.html'
    context_object_name = 'secciones'

    def get_queryset(self):
        return Seccion.objects.filter(
            propuesta_asamblea=self.request.user.asamblea.propuestaasamblea
        ).order_by('-fecha_actualizacion')

    def get_context_data(self, **kwargs):
        context = super(
            ListaSeccionesPropuesta, self
        ).get_context_data(**kwargs) # default
        context['propuesta_asamblea_id'] = (
            self.request.user.asamblea.propuestaasamblea.id
        )
        if self.request.user.asamblea.propuestaasamblea.en_aprobacion==True:
            context['estado_votaciones']='Las votaciones están Activadas'
            context['texto_boton']='Desactivar Votaciones'
        else:
            context['estado_votaciones']='Las votaciones están Desactivadas'
            context['texto_boton']='Activar Votaciones'
        return context

    def test_func(self):
        return es_representante(self.request.user)


# U de CRUD
class EditarSeccionPropuesta(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, 
    BorrarVotacionesMixin, UpdateView
):
    
    model = Seccion
    template_name = 'asambleas/editar_seccion.html'
    fields = ['tema','titulo','texto']
    success_url = reverse_lazy('asambleas:lista_secciones_propuesta')
    success_message = (
        'APROBACIONES BORRADAS: '
        'Debe solicitar aprobaciones nuevamente!'
    )

    def test_func(self):
        return es_representante(self.request.user)


# D de CRUD
class EliminarSeccionPropuesta(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, 
    BorrarVotacionesMixin, DeleteView
):
    
    model = Seccion
    context_object_name = 'seccion'
    template_name = 'asambleas/eliminar_seccion.html'
    success_url = reverse_lazy('asambleas:lista_secciones_propuesta')
    success_message = (
        'APROBACIONES BORRADAS:'
        'Debe solicitar aprobaciones nuevamente!'
    )

    def test_func(self):
        return es_representante(self.request.user)

# CRUD Secciones Individuales


# C de CRUD
class CrearSeccionIndividual(LoginRequiredMixin, 
                            UserPassesTestMixin, 
                            CreateView):
    model = SeccionIndividual
    fields = ['tema', 'titulo', 'texto']
    template_name = 'asambleas/crear_seccion_individual.html'
    #success_message = 'APROBACIONES BORRADAS: Debe solicitar aprobaciones nuevamente!'
    success_url = reverse_lazy('asambleas:lista_secciones_individuales')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearSeccionIndividual, self).form_valid(form)

    def test_func(self):
        return es_miembro(self.request.user)


# R de CRUD
class ListaSeccionesIndividuales(LoginRequiredMixin, 
                            UserPassesTestMixin, 
                            ListView):
    model = SeccionIndividual
    template_name = 'asambleas/lista_secciones_individuales.html'
    context_object_name = 'secciones'

    def get_queryset(self):
        return SeccionIndividual.objects.filter(
            usuario=self.request.user
        ).order_by('-fecha_creacion')

    def test_func(self):
        return es_miembro(self.request.user)


# U de CRUD

# D de CRUD

from .forms import FormularioAprobacionPA
from gestion.models import AprobacionPA
# Ver Propuesta Asamblea
class VerPropuestaAsamblea(
    LoginRequiredMixin, UserPassesTestMixin, ListView
):
    
    model = Seccion
    template_name = 'asambleas/ver_propuesta_asamblea.html'
    context_object_name = 'secciones'
    form_class = FormularioAprobacionPA
    model_aprobacion = AprobacionPA

    def get_queryset(self):
        return Seccion.objects.filter(
            propuesta_asamblea=self.request.user.asamblea.propuestaasamblea
        ).order_by('-fecha_actualizacion')

    def get_context_data(self, **kwargs):
        context = super(VerPropuestaAsamblea, self).get_context_data(**kwargs) # default
        context['asamblea'] = self.request.user.asamblea # objeto extra
        context['form'] = self.form_class
        context['num_aprobaciones'] = len(self.model_aprobacion.objects.filter(tipo=1))
        context['num_rechazos'] = len(self.model_aprobacion.objects.filter(tipo=2))
        if (len(self.model_aprobacion.objects.filter(usuario=self.request.user))==0 and 
                self.request.user.asamblea.propuestaasamblea.en_aprobacion==True):
            context['mostrar_voto'] = True
            context['bloqueada']=False
        elif (len(self.model_aprobacion.objects.filter(usuario=self.request.user))!=0 and 
                self.request.user.asamblea.propuestaasamblea.en_aprobacion==True):
            context['mostrar_voto'] = False
            context['bloqueada']=False
            context['voto'] = self.model_aprobacion.objects.get(usuario=self.request.user).get_tipo_display()
        elif (len(self.model_aprobacion.objects.filter(usuario=self.request.user))!=0 and 
                self.request.user.asamblea.propuestaasamblea.en_aprobacion==False):
            context['mostrar_voto'] = False
            context['bloqueada']=True
        elif (len(self.model_aprobacion.objects.filter(usuario=self.request.user))==0 and 
                self.request.user.asamblea.propuestaasamblea.en_aprobacion==False):
            context['mostrar_voto'] = False
            context['bloqueada']=True

        print(context)
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
        context['num_aprobaciones'] = len(self.model_aprobacion.objects.filter(tipo=1))
        context['num_rechazos'] = len(self.model_aprobacion.objects.filter(tipo=2))
        if (len(self.model_aprobacion.objects.filter(usuario=self.request.user))==0 and 
                self.request.user.asamblea.propuestaasamblea.en_aprobacion==True):
            context['mostrar_voto'] = True
            context['bloqueada']=False
        elif (len(self.model_aprobacion.objects.filter(usuario=self.request.user))!=0 and 
                self.request.user.asamblea.propuestaasamblea.en_aprobacion==True):
            context['mostrar_voto'] = False
            context['bloqueada']=False
            context['voto'] = self.model_aprobacion.objects.get(usuario=self.request.user).get_tipo_display()
        elif (len(self.model_aprobacion.objects.filter(usuario=self.request.user))!=0 and 
                self.request.user.asamblea.propuestaasamblea.en_aprobacion==False):
            context['mostrar_voto'] = False
            context['bloqueada']=True
        elif (len(self.model_aprobacion.objects.filter(usuario=self.request.user))==0 and 
                self.request.user.asamblea.propuestaasamblea.en_aprobacion==False):
            context['mostrar_voto'] = False
            context['bloqueada']=True
        return render(self.request, self.template_name, context)

    def test_func(self):
        return es_miembro(self.request.user) or es_representante(self.request.user)



# Ver Secciones Individuales de la Asamblea
class VerSeccionesIndividuales(
    LoginRequiredMixin, UserPassesTestMixin, ListView
):
    
    model = SeccionIndividual
    template_name = 'asambleas/ver_secciones_individuales_de_asamblea.html'
    context_object_name = 'secciones'

    def get_queryset(self):
        asamblea = self.request.user.asamblea
        usuarios_asamblea = asamblea.usuario_set.all()
        print(usuarios_asamblea)
        return SeccionIndividual.objects.filter(
            usuario__in=usuarios_asamblea
        ).order_by('-fecha_creacion')

    def test_func(self):
        return es_representante(self.request.user)

#------------------------------------------------------------------------------
# CRUD Asambleas para Administrador

# C de CRUD
class CrearAsamblea(
    LoginRequiredMixin, UserPassesTestMixin, CreateView
):
    
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

    def test_func(self):
        return es_administrador(self.request.user)


# R de CRUD
class ListaAsambleas(
    LoginRequiredMixin, UserPassesTestMixin, ListView
):
    
    model = Asamblea
    template_name = 'asambleas/lista_asambleas.html'
    context_object_name = 'asambleas'

    def get_context_data(self, **kwargs):
        context = super(ListaAsambleas, self).get_context_data(**kwargs) # default
        context['asambleas']=context['asambleas'].order_by('id')
        representantes=list()
        for asamblea in context['asambleas']:
            representante_querylist=User.objects.filter(asamblea=asamblea).filter(rol__nombre="Representante")
            print(representante_querylist)
            if len(representante_querylist)==0:
                representantes.append("Sin Definir")
            else:
                representantes.append(representante_querylist[0])
        print(representantes)
        context['asambleas_representantes']=zip(list(context['asambleas']),representantes)
        return context

    def test_func(self):
        return es_administrador(self.request.user)


# U de CRUD
class EditarAsamblea(
    LoginRequiredMixin, UserPassesTestMixin, UpdateView
):
    
    model = Asamblea
    form_class = EditarAsambleaForm
    template_name = 'asambleas/editar_asamblea.html'
    #fields = ['nombre','descripcion','telefono','email','direccion_calle','direccion_numero','comuna']
    success_url = reverse_lazy('asambleas:lista_asambleas')
    
    def form_valid(self, form):
        form.instance.representante = form.cleaned_data['representante']
        usuario_representante = User.objects.get(id=int(form.instance.representante))
        usuarios_asamblea = User.objects.filter(asamblea=usuario_representante.asamblea)
        # setea todos los usuarios de esta asamblea a miembros
        usuarios_asamblea.update(rol=Rol.objects.get(nombre="Miembro"))
        # setea el usuario escogido como representante
        usuario_representante.rol=Rol.objects.get(nombre="Representante")
        usuario_representante.save()
        return super(EditarAsamblea, self).form_valid(form)

    def test_func(self):
        return es_administrador(self.request.user)

# D de CRUD


#------------------------------------------------------------------------------
# Activar / Desactivar Votaciones
from django.http import HttpResponse
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


@login_required
@require_POST
def voto_toggle(request):
    if request.method == 'POST':
        user = request.user
        slug = request.POST.get('slug', None)
        #company = get_object_or_404(Asamblea, slug=slug)
        propuesta_asamblea = get_object_or_404(PropuestaAsamblea, id=slug)
        if propuesta_asamblea.en_aprobacion==False:
            # user has already liked this company
            # remove like/user
            propuesta_asamblea.en_aprobacion=True
            propuesta_asamblea.save()
            message = 'Has Activado las Votaciones'
        else:
            # add a new like for a company
            propuesta_asamblea.en_aprobacion=False
            propuesta_asamblea.save()
            message = 'Has Desactivado las Votaciones'

    ctx = {'message': message}
    if request.user.asamblea.propuestaasamblea.en_aprobacion==True:
        ctx['estado_votaciones']='Las votaciones están Activadas'
        ctx['texto_boton']='Desactivar Votaciones'
    else:
        ctx['estado_votaciones']='Las votaciones están Desactivadas'
        ctx['texto_boton']='Activar Votaciones'
    print(ctx)
# use mimetype instead of content_type if django < 5
    return HttpResponse(json.dumps(ctx), content_type='application/json')



# CRUD Usuarios

# R de CRUD

class ListaUsuarios(
    LoginRequiredMixin, UserPassesTestMixin, ListView
):
    
    model = User
    template_name = 'asambleas/lista_usuarios.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        return User.objects.filter(asamblea=self.request.user.asamblea)

    def test_func(self):
        return (
            es_administrador(self.request.user) 
            or es_representante(self.request.user) 
            or es_miembro(self.request.user)
        )