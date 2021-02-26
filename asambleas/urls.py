from django.urls import path
from . import views

app_name = "asambleas"

urlpatterns = [
    path('', views.principal, name="principal"),
]