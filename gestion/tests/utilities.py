from django.test import TestCase
from gestion.models import (
    Rol,Distrito, Comuna, Asamblea, PropuestaAsamblea
)


class BaseDataTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        for element in Distrito.objects.all().values():
            print(element)
        if len(Rol.objects.all()) < 1:
            Rol.objects.create(
                nombre = "Miembro", 
                descripcion = (
                    "Ciudadano perteneciente" 
                    " a una asamblea territorial"
                )
            )
            Rol.objects.create(
                nombre = "Representante", 
                descripcion = (
                    "Ciudadano representante" 
                    " de una asamblea territorial"
                )
            )
            Rol.objects.create(
                nombre = "Administrador", 
                descripcion = (
                    "Ciudadano administrador"
                    " de una asamblea territorial"
                )
            )
            Rol.objects.create(
                nombre = "Superadmin", 
                descripcion = (
                    "Usuario administrador"
                    " de la plataforma ConverGente"
                )
            )

        if len(Distrito.objects.all())<1:
            Distrito.objects.create(nombre = "Santiago Cordillera", numero="14")
            Distrito.objects.create(nombre = "Santiago Sur", numero="15")
            Distrito.objects.create(nombre = "Santiago Norte", numero="16")
            Distrito.objects.create(nombre = "Santiago Oriente", numero="17")
            Distrito.objects.create(nombre = "Santiago Poniente", numero="18")

            distrito_14=Distrito.objects.get(numero = "14")
            distrito_15=Distrito.objects.get(numero = "15")
            distrito_16=Distrito.objects.get(numero = "16")
            distrito_17=Distrito.objects.get(numero = "17")
            distrito_18=Distrito.objects.get(numero = "18")

        if len(Comuna.objects.all()) < 1:
            Comuna.objects.create(
                nombre = "Peñalolén", 
                region = "13", 
                distrito = distrito_14
            )
            Comuna.objects.create(
                nombre = "Lo Barnechea", 
                region = "13", 
                distrito = distrito_14
            )
            Comuna.objects.create(
                nombre = "San José de Maipo", 
                region = "13", 
                distrito = distrito_14
            )
            Comuna.objects.create(
                nombre = "San Bernardo", 
                region = "13", 
                distrito = distrito_15
            )
            Comuna.objects.create(
                nombre = "San Miguel", 
                region = "13", 
                distrito = distrito_15
            )
            Comuna.objects.create(
                nombre = "La Cisterna", 
                region = "13", 
                distrito = distrito_15
            )
            Comuna.objects.create(
                nombre = "La Pintana", 
                region = "13", 
                distrito = distrito_15
            )
            Comuna.objects.create(
                nombre = "Recoleta", 
                region = "13", 
                distrito = distrito_16
            )
            Comuna.objects.create(
                nombre = "Independencia", 
                region = "13", 
                distrito = distrito_16
            )
            Comuna.objects.create(
                nombre = "Quilicura", 
                region = "13", 
                distrito = distrito_16
            )
            Comuna.objects.create(
                nombre = "Renca", 
                region = "13", 
                distrito = distrito_16
            )
            Comuna.objects.create(
                nombre = "Las Condes", 
                region = "13", 
                distrito = distrito_17
            )
            Comuna.objects.create(
                nombre = "La Reina", 
                region = "13", 
                distrito = distrito_17
            )
            Comuna.objects.create(
                nombre = "Ñuñoa", 
                region = "13", 
                distrito = distrito_17
            )
            Comuna.objects.create(
                nombre = "Vitacura", 
                region = "13", 
                distrito = distrito_17
            )
            Comuna.objects.create(
                nombre = "Maipú", 
                region = "13", 
                distrito = distrito_18
            )
            Comuna.objects.create(
                nombre = "Padre Hurtado", 
                region = "13", 
                distrito = distrito_18
            )
            Comuna.objects.create(
                nombre = "El Monte", 
                region = "13", 
                distrito = distrito_18
            )
            Comuna.objects.create(
                nombre = "Pudahuel", 
                region = "13", 
                distrito = distrito_18
            )

        if len(Asamblea.objects.all()) < 1:
            for index in [1,2,3,4,5,6]:
                Asamblea.objects.create(
                    nombre = "Genesis" + str(index), 
                    descripcion = (
                        "Esta es la descripción"
                        " de la Asamblea Genesis" + str(index)
                    ), 
                    telefono = "+56000000000",
                    email = "asablea@gmail.com", 
                    direccion_calle = "Avenida Acacia - Genesis"+str(index), 
                    direccion_numero = "22", 
                    comuna = Comuna.objects.all()[index-1]
                )

        if len(PropuestaAsamblea.objects.all())<1:
            for index in [1,2,3,4,5,6]:
                PropuestaAsamblea.objects.create(
                    titulo = (
                        "Título de propuesta de asamblea Genesis" + str(index)
                    ),
                    descripcion = (
                        "Descripcion de propuesta"
                        " de asamble Genesis" + str(index)
                    ),
                    asamblea=Asamblea.objects.all()[index-1]
                )