from django.urls import path
from . import views

app_name = "gestion"

urlpatterns = [
    path('registro/', views.registro, name="registro"),
]