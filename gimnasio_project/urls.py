
from django.contrib import admin
from django.urls import path
from core.views.cliente import cliente_create, cliente_delete, cliente_list, cliente_update
from core.views.home import home  # Importar la vista home
from core.views import rutina, seguimiento_rutina

from core.views.inscripcion import (
    inscripcion_list,
    inscripcion_create,
    inscripcion_update,
    inscripcion_delete
)
from core.views import membresia
from core.views.tipomembresia import (
    tipo_membresia_list,
    tipo_membresia_create,
    tipo_membresia_update,
    tipo_membresia_delete
)



from core.views.condicion import condicion_create, condicion_list, condicion_delete, condicion_update
from core.views.rol import rol_create, rol_list, rol_delete, rol_update
from core.views.empleado import empleado_list, empleado_create, empleado_update, empleado_delete
from core.views.evaluacion import evaluacion_list, evaluacion_create, evaluacion_update, evaluacion_delete





urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home
    path('', home, name='home'),  # Ruta principal
    
    # Clientes
    path('clientes/', cliente_list, name='cliente_list'),
    path('clientes/nuevo/', cliente_create, name='cliente_create'),
    path('clientes/<int:id_cliente>/editar/', cliente_update, name='cliente_update'),
    path('clientes/<int:id_cliente>/eliminar/', cliente_delete, name='cliente_delete'),
    
    # Inscripciones
    path('inscripciones/', inscripcion_list, name='inscripcion_list'),
    path('inscripciones/nuevo/', inscripcion_create, name='inscripcion_create'),
    path('inscripciones/<int:id_inscripcion>/editar/', inscripcion_update, name='inscripcion_update'),
    path('inscripciones/<int:id_inscripcion>/eliminar/', inscripcion_delete, name='inscripcion_delete'),
    
    # Membresías
    path('membresias/', membresia.membresia_list, name='membresia_list'),
    path('membresias/nueva/', membresia.membresia_create, name='membresia_create'),
    path('membresias/<int:id_membresia>/editar/', membresia.membresia_update, name='membresia_update'),
    path('membresias/<int:id_membresia>/eliminar/', membresia.membresia_delete, name='membresia_delete'),
    
    # Tipos de Membresía
    path('tiposmembresia/', tipo_membresia_list, name='tipo_membresia_list'),
    path('tiposmembresia/nuevo/', tipo_membresia_create, name='tipo_membresia_create'),
    path('tiposmembresia/<int:id_tipo_membresia>/editar/', tipo_membresia_update, name='tipo_membresia_update'),
    path('tiposmembresia/<int:id_tipo_membresia>/eliminar/', tipo_membresia_delete, name='tipo_membresia_delete'),
    
    # Rutas para las vistas de rutina y seguimiento de rutina
    path('rutinas/', rutina.rutina_list, name='rutina_list'),
    path('rutinas/create/', rutina.rutina_create, name='rutina_create'),
    path('rutinas/update/<int:id_rutina>/', rutina.rutina_update, name='rutina_update'),
    path('rutinas/delete/<int:id_rutina>/', rutina.rutina_delete, name='rutina_delete'),

    path('seguimiento_rutinas/', seguimiento_rutina.seguimiento_rutina_list, name='seguimiento_rutina_list'),
    path('seguimiento_rutinas/create/', seguimiento_rutina.seguimiento_rutina_create, name='seguimiento_rutina_create'),
    path('seguimiento_rutinas/update/<int:id_seguimiento>/', seguimiento_rutina.seguimiento_rutina_update, name='seguimiento_rutina_update'),
    path('seguimiento_rutinas/delete/<int:id_seguimiento>/', seguimiento_rutina.seguimiento_rutina_delete, name='seguimiento_rutina_delete'),
    
    
    path('condiciones/', condicion_list, name='condicion_list'),
    path('condiciones/nuevo/', condicion_create, name='condicion_create'),
    path('condiciones/<int:id_condicion_fisica>/eliminar/', condicion_delete, name='condicion_delete'),
    path('condiciones/<int:id_cliente>/editar/', condicion_update, name='condicion_update'),
    path('roles/', rol_list, name='rol_list'),
    path('roles/nuevo/', rol_create, name='rol_create'),
    path('roles/<int:id_rol>/editar/', rol_update, name='rol_update'),
    path('roles/<int:id_rol>/eliminar/', rol_delete, name='rol_delete'),

 
    # urls.py
    path('condiciones/<int:id_condicion_fisica>/editar/', condicion_update, name='condicion_update'),
    path('condiciones/<int:id_condicion_fisica>/eliminar/', condicion_delete, name='condicion_delete'),

    path('empleados/', empleado_list, name='empleado_list'),
    path('empleados/nuevo/', empleado_create, name='empleado_create'),
    path('empleados/<int:id_empleado>/editar/', empleado_update, name='empleado_update'),
    path('empleados/<int:id_empleado>/eliminar/', empleado_delete, name='empleado_delete'),
    path('evaluaciones/', evaluacion_list, name='evaluacion_list'),
    path('evaluaciones/nuevo/', evaluacion_create, name='evaluacion_create'),
    path('evaluaciones/<int:id_evaluacion>/editar/', evaluacion_update, name='evaluacion_update'),
    path('evaluaciones/<int:id_evaluacion>/eliminar/', evaluacion_delete, name='evaluacion_delete'),
    
    
    
    
]































# from django.contrib import admin
# from django.urls import path
# from core.views.cliente import cliente_create, cliente_delete, cliente_list, cliente_update

# from core.views import rutina, seguimiento_rutina


# from core.views.inscripcion import (
#     inscripcion_list,
#     inscripcion_create,
#     inscripcion_update,
#     inscripcion_delete
# )
# from core.views import membresia
# from core.views.tipomembresia import (
#     tipo_membresia_list,
#     tipo_membresia_create,
#     tipo_membresia_update,
#     tipo_membresia_delete
# )

# urlpatterns = [
#     path('admin/', admin.site.urls),
    
#     # Clientes
#     path('clientes/', cliente_list, name='cliente_list'),
#     path('clientes/nuevo/', cliente_create, name='cliente_create'),
#     path('clientes/<int:id_cliente>/editar/', cliente_update, name='cliente_update'),
#     path('clientes/<int:id_cliente>/eliminar/', cliente_delete, name='cliente_delete'),
    
#     # Inscripciones
#     path('inscripciones/', inscripcion_list, name='inscripcion_list'),
#     path('inscripciones/nuevo/', inscripcion_create, name='inscripcion_create'),
#     path('inscripciones/<int:id_inscripcion>/editar/', inscripcion_update, name='inscripcion_update'),
#     path('inscripciones/<int:id_inscripcion>/eliminar/', inscripcion_delete, name='inscripcion_delete'),
    
#     # Membresías
#     path('membresias/', membresia.membresia_list, name='membresia_list'),
#     path('membresias/nueva/', membresia.membresia_create, name='membresia_create'),
#     path('membresias/<int:id_membresia>/editar/', membresia.membresia_update, name='membresia_update'),
#     path('membresias/<int:id_membresia>/eliminar/', membresia.membresia_delete, name='membresia_delete'),
    
#     # Tipos de Membresía
#     path('tiposmembresia/', tipo_membresia_list, name='tipo_membresia_list'),
#     path('tiposmembresia/nuevo/', tipo_membresia_create, name='tipo_membresia_create'),
#     path('tiposmembresia/<int:id_tipo_membresia>/editar/', tipo_membresia_update, name='tipo_membresia_update'),
#     path('tiposmembresia/<int:id_tipo_membresia>/eliminar/', tipo_membresia_delete, name='tipo_membresia_delete'),
    
#     # Rutas para las vistas de rutina y seguimiento de rutina
#     path('rutinas/', rutina.rutina_list, name='rutina_list'),
#     path('rutinas/create/', rutina.rutina_create, name='rutina_create'),
#     path('rutinas/update/<int:id_rutina>/', rutina.rutina_update, name='rutina_update'),
#     path('rutinas/delete/<int:id_rutina>/', rutina.rutina_delete, name='rutina_delete'),

#     path('seguimiento_rutinas/', seguimiento_rutina.seguimiento_rutina_list, name='seguimiento_rutina_list'),
#     path('seguimiento_rutinas/create/', seguimiento_rutina.seguimiento_rutina_create, name='seguimiento_rutina_create'),
#     path('seguimiento_rutinas/update/<int:id_seguimiento>/', seguimiento_rutina.seguimiento_rutina_update, name='seguimiento_rutina_update'),
#     path('seguimiento_rutinas/delete/<int:id_seguimiento>/', seguimiento_rutina.seguimiento_rutina_delete, name='seguimiento_rutina_delete'),
# ]