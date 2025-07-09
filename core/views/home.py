# core/views/home.py
from django.shortcuts import render

def home(request):
    """
    Vista principal del sistema de gestión de gimnasio
    """
    context = {
        'title': 'Sistema de Gestión de Gimnasio',
        'sections': [
            {
                'name': 'Clientes',
                'icon': 'fas fa-users',
                'description': 'Gestión de clientes del gimnasio',
                'urls': [
                    {'name': 'Ver Clientes', 'url': 'cliente_list', 'icon': 'fas fa-list'},
                    {'name': 'Nuevo Cliente', 'url': 'cliente_create', 'icon': 'fas fa-plus'},
                ]
            },
            {
                'name': 'Inscripciones',
                'icon': 'fas fa-clipboard-list',
                'description': 'Gestión de inscripciones',
                'urls': [
                    {'name': 'Ver Inscripciones', 'url': 'inscripcion_list', 'icon': 'fas fa-list'},
                    {'name': 'Nueva Inscripción', 'url': 'inscripcion_create', 'icon': 'fas fa-plus'},
                ]
            },
            {
                'name': 'Membresías',
                'icon': 'fas fa-id-card',
                'description': 'Gestión de membresías',
                'urls': [
                    {'name': 'Ver Membresías', 'url': 'membresia_list', 'icon': 'fas fa-list'},
                    {'name': 'Nueva Membresía', 'url': 'membresia_create', 'icon': 'fas fa-plus'},
                ]
            },
            {
                'name': 'Tipos de Membresía',
                'icon': 'fas fa-tags',
                'description': 'Gestión de tipos de membresía',
                'urls': [
                    {'name': 'Ver Tipos', 'url': 'tipo_membresia_list', 'icon': 'fas fa-list'},
                    {'name': 'Nuevo Tipo', 'url': 'tipo_membresia_create', 'icon': 'fas fa-plus'},
                ]
            },
            {
                'name': 'Rutinas',
                'icon': 'fas fa-dumbbell',
                'description': 'Gestión de rutinas de ejercicios',
                'urls': [
                    {'name': 'Ver Rutinas', 'url': 'rutina_list', 'icon': 'fas fa-list'},
                    {'name': 'Nueva Rutina', 'url': 'rutina_create', 'icon': 'fas fa-plus'},
                ]
            },
            {
                'name': 'Seguimiento de Rutinas',
                'icon': 'fas fa-chart-line',
                'description': 'Seguimiento y progreso de rutinas',
                'urls': [
                    {'name': 'Ver Seguimientos', 'url': 'seguimiento_rutina_list', 'icon': 'fas fa-list'},
                    {'name': 'Nuevo Seguimiento', 'url': 'seguimiento_rutina_create', 'icon': 'fas fa-plus'},
                ]
            },
        ]
    }
    return render(request, 'home.html', context)