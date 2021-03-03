from django.contrib import admin
from .models import PropuestaAsamblea

# Register your models here.
class PropuestaAsambleaAdmin(admin.ModelAdmin):
    list_display=('titulo', 'descripcion', 'asamblea', 'usuario_actualizacion')

admin.site.register(PropuestaAsamblea, PropuestaAsambleaAdmin)
