"""
URL configuration for gimnasio_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))


"""


from django.contrib import admin
from django.urls import path
from core.views.cliente import cliente_create, cliente_delete, cliente_list, cliente_update
from core.views.inscripcion import (
    inscripcion_list,
    inscripcion_create,
    inscripcion_update,
    inscripcion_delete
)

from core.views import membresia
urlpatterns = [
    path('admin/', admin.site.urls),
    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<int:id_cliente>/editar/', cliente_update, name='cliente_update'),
    path('clientes/<int:id_cliente>/eliminar/', cliente_delete, name='cliente_delete'),
    path('inscripciones/', inscripcion_list, name='inscripcion_list'),
    path('inscripciones/nuevo/', inscripcion_create, name='inscripcion_create'),
    path('inscripciones/<int:id_inscripcion>/editar/', inscripcion_update, name='inscripcion_update'),
    path('inscripciones/<int:id_inscripcion>/eliminar/', inscripcion_delete, name='inscripcion_delete'),
    path('membresias/', membresia.membresia_list, name='membresia_list'),
    path('membresias/nueva/', membresia.membresia_create, name='membresia_create'),
    path('membresias/<int:id_membresia>/editar/', membresia.membresia_update, name='membresia_update'),
    path('membresias/<int:id_membresia>/eliminar/', membresia.membresia_delete, name='membresia_delete'),
]






