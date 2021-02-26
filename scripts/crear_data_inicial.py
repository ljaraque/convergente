from django.contrib.auth import get_user_model
User = get_user_model()
from gestion.models import Rol,Distrito, Comuna, Asamblea, Tema

def crear():

    if len(Rol.objects.all())<1:
        Rol.objects.create(nombre="Miembro", descripcion="Ciudadano perteneciente a una asamblea territorial")
        Rol.objects.create(nombre="Representante", descripcion="Ciudadano representante de una asamblea territorial")
        Rol.objects.create(nombre="Superadmin", descripcion="Usuario administrador de la plataforma ConverGente")

    if len(Distrito.objects.all())<1:
        Distrito.objects.create(nombre="Santiago Cordillera", numero="14")
        Distrito.objects.create(nombre="Santiago Sur", numero="15")
        Distrito.objects.create(nombre="Santiago Norte", numero="16")
        Distrito.objects.create(nombre="Santiago Oriente", numero="17")
        Distrito.objects.create(nombre="Santiago Poniente", numero="18")

    if len(Comuna.objects.all())<1:
        distrito_14=Distrito.objects.get(numero="14")
        distrito_15=Distrito.objects.get(numero="15")
        distrito_16=Distrito.objects.get(numero="16")
        distrito_17=Distrito.objects.get(numero="17")
        distrito_18=Distrito.objects.get(numero="18")

        Comuna.objects.create(nombre="Peñalolén", region="13", distrito=distrito_14)
        Comuna.objects.create(nombre="Lo Barnechea", region="13", distrito=distrito_14)
        Comuna.objects.create(nombre="San José de Maipo", region="13", distrito=distrito_14)
        Comuna.objects.create(nombre="San Bernardo", region="13", distrito=distrito_15)
        Comuna.objects.create(nombre="San Miguel", region="13", distrito=distrito_15)
        Comuna.objects.create(nombre="La Cisterna", region="13", distrito=distrito_15)
        Comuna.objects.create(nombre="La Pintana", region="13", distrito=distrito_15)
        Comuna.objects.create(nombre="Recoleta", region="13", distrito=distrito_16)
        Comuna.objects.create(nombre="Independencia", region="13", distrito=distrito_16)
        Comuna.objects.create(nombre="Quilicura", region="13", distrito=distrito_16)
        Comuna.objects.create(nombre="Renca", region="13", distrito=distrito_16)
        Comuna.objects.create(nombre="Las Condes", region="13", distrito=distrito_17)
        Comuna.objects.create(nombre="La Reina", region="13", distrito=distrito_17)
        Comuna.objects.create(nombre="Ñuñoa", region="13", distrito=distrito_17)
        Comuna.objects.create(nombre="Vitacura", region="13", distrito=distrito_17)
        Comuna.objects.create(nombre="Maipú", region="13", distrito=distrito_18)
        Comuna.objects.create(nombre="Padre Hurtado", region="13", distrito=distrito_18)
        Comuna.objects.create(nombre="El Monte", region="13", distrito=distrito_18)
        Comuna.objects.create(nombre="Pudahuel", region="13", distrito=distrito_18)

    if len(Asamblea.objects.all())<1:
        for index in [1,2,3,4,5,6]:
            Asamblea.objects.create(nombre="Genesis"+str(index), 
                                    descripcion="Esta es la descripción de la Asamblea Genesis"+str(index), 
                                    telefono="+56000000000",
                                    email="asablea@gmail.com", 
                                    direccion_calle="Avenida Acacia - Genesis"+str(index), 
                                    direccion_numero="22", 
                                    comuna=Comuna.objects.all()[index-1])

    if len(User.objects.all())<1:
        for index in [1,2,3,4,5,6]:
            User.objects.create_user(username="Neo"+str(index),
                                rut="12345678-"+str(index),
                                first_name="Neo"+str(index),
                                apellido_paterno="NeoAp",
                                apellido_materno="NeoAp",
                                resumen="Soy Neo",
                                telefono="+56000000000",
                                sexo=User.FEMENINO,
                                estado_civil=User.SOLTERO,
                                direccion_calle="Calle",
                                direccion_numero="000",
                                comuna=Asamblea.objects.all()[index-1].comuna,
                                asamblea=Asamblea.objects.all()[index-1],
                                password="1234", 
                                rol=Rol.objects.get(nombre="Representante"))

            User.objects.create_user(username="Alan"+str(index),
                                rut="22345678-"+str(index),
                                first_name="Alan"+str(index),
                                apellido_paterno="AlanAp",
                                apellido_materno="AlanAp",
                                resumen="Soy Alan",
                                telefono="+56000000000",
                                sexo=User.MASCULINO,
                                estado_civil=User.SOLTERO,
                                direccion_calle="Calle",
                                direccion_numero="000",
                                comuna=Asamblea.objects.all()[0].comuna,
                                asamblea=Asamblea.objects.all()[0],
                                password="1234", 
                                rol=Rol.objects.get(nombre="Miembro"))


    if len(Tema.objects.all())<1:
        Tema.objects.create(nombre="Eduación")
        Tema.objects.create(nombre="Salud")
        Tema.objects.create(nombre="Vivienda")
        Tema.objects.create(nombre="Medio Ambiente")
        Tema.objects.create(nombre="Previsión")
        Tema.objects.create(nombre="Trabajo")
        Tema.objects.create(nombre="Género")
        Tema.objects.create(nombre="Plurinacionalidad")
        Tema.objects.create(nombre="Derechos Humanos")
        Tema.objects.create(nombre="Niñez")
        Tema.objects.create(nombre="Ciencia y Tecnología")
        Tema.objects.create(nombre="Sistema Económico")
        Tema.objects.create(nombre="Sistema Político")
        Tema.objects.create(nombre="Relaciones Internacionales")
