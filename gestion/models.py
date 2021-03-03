from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Distrito(models.Model):
    nombre = models.CharField(max_length=100)
    numero = models.IntegerField() 


class Comuna(models.Model):
    nombre = models.CharField(max_length=100)
    region = models.CharField(max_length=200)
    
    #related
    distrito = models.ForeignKey(Distrito, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nombre


class Asamblea(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=300)
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    direccion_calle = models.CharField(max_length=200)
    direccion_numero = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    #related
    comuna = models.ForeignKey(Comuna, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "Código: "+str(self.id) + ", Nombre: " + self.nombre


class Rol(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(max_length=300)

    def __str__(self):
        return self.nombre


class Usuario(AbstractUser):
    SOLTERO = 1
    CASADO = 2
    SEPARADO = 3
    DIVORCIADO = 4
    VIUDO = 5
    ESTADO_CIVIL_CHOICES = [
        (SOLTERO, 'Solter@'),
        (CASADO, 'Casad@'),
        (SEPARADO, 'Separad@'),
        (DIVORCIADO, 'Divorciad@'),
        (VIUDO, 'Viud@'),
    ]
    FEMENINO='F'
    MASCULINO='M'
    SEXO_CHOICES = [
        (FEMENINO, 'Femenino'),
        (MASCULINO, 'Masculino')
    ]
    apellido_paterno = models.CharField(max_length=50, null=True, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=50, null=True, verbose_name="Apellido Materno")
    rut = models.CharField(max_length=12, unique=True)
    resumen = models.TextField(max_length=300)
    telefono = models.CharField(max_length=20)
    sexo = models.CharField(max_length=1, choices=SEXO_CHOICES)
    estado_civil = models.IntegerField(choices=ESTADO_CIVIL_CHOICES, default=SOLTERO)
    direccion_calle = models.CharField(max_length=200)
    direccion_numero = models.CharField(max_length=50)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    # related
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    representante = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    asamblea = models.ForeignKey(Asamblea, on_delete=models.DO_NOTHING)
    comuna = models.ForeignKey(Comuna, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.first_name + " " + self.apellido_paterno + " - Rut: " + self.rut

class Tema(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class PropuestaAsamblea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(max_length=300)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    #related
    asamblea = models.OneToOneField(Asamblea, null=True, on_delete=models.DO_NOTHING)
    usuario_actualizacion = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)


class SeccionIndividual(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField(max_length=2000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    #related
    usuario = models.ForeignKey(Usuario, null=True, on_delete=models.SET_NULL)
    tema = models.ForeignKey(Tema, null=True, on_delete=models.SET_NULL)


class Seccion(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField(max_length=2000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    #related
    tema = models.ForeignKey(Tema, on_delete=models.DO_NOTHING)
    propuesta_asamblea = models.ForeignKey(PropuestaAsamblea, on_delete=models.CASCADE)


class AprobacionPA(models.Model):
    APRUEBA = 1
    RECHAZA = 2
    TIPO_CHOICES = [
        (APRUEBA, 'Aprueba'),
        (RECHAZA, 'Rechaza'),
    ]
    tipo = models.IntegerField(choices=TIPO_CHOICES, default=APRUEBA)
    comentario = models.TextField(max_length=1000)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    #related
    propuesta_asamblea = models.ForeignKey(PropuestaAsamblea, on_delete=models.CASCADE)
    usuario = models.OneToOneField(Usuario, models.CASCADE)

