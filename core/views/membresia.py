from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.forms import MembresiaForm
from core.models import SggMMembresia
import pyodbc
from django.db import connection

def membresia_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT m.id_membresia, t.nombre AS tipo, d.nombre AS duracion, m.precio_actual, m.descripcion
            FROM SGG_M_Membresia m
            JOIN SGG_P_TipoMembresia t ON m.id_tipo_membresia = t.id_tipo_membresia
            JOIN SGG_P_Duracion d ON m.id_duracion = d.id_duracion
        """)
        membresias = cursor.fetchall()
    return render(request, 'membresia/list.html', {'membresias': membresias})

def membresia_create(request):
    if request.method == 'POST':
        form = MembresiaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO SGG_M_Membresia (id_tipo_membresia, id_duracion, precio_actual, descripcion)
                    VALUES (?, ?, ?, ?)
                """, (data['id_tipo_membresia'], data['id_duracion'], data['precio_actual'], data['descripcion']))
            messages.success(request, 'Membresía registrada exitosamente.')
            return redirect('membresia_list')
    else:
        form = MembresiaForm()
    return render(request, 'membresia/form.html', {'form': form, 'title': 'Registrar membresía', 'back_url': 'membresia_list'})

def membresia_update(request, id_membresia):
    membresia = get_object_or_404(SggMMembresia, pk=id_membresia)
    if request.method == 'POST':
        form = MembresiaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE SGG_M_Membresia SET id_tipo_membresia = ?, id_duracion = ?, precio_actual = ?, descripcion = ?
                    WHERE id_membresia = ?
                """, (data['id_tipo_membresia'], data['id_duracion'], data['precio_actual'], data['descripcion'], id_membresia))
            messages.success(request, 'Membresía actualizada.')
            return redirect('membresia_list')
    else:
        form = MembresiaForm(initial={
            'id_tipo_membresia': membresia.id_tipo_membresia_id,
            'id_duracion': membresia.id_duracion_id,
            'precio_actual': membresia.precio_actual,
            'descripcion': membresia.descripcion,
        })
    return render(request, 'membresia/form.html', {'form': form, 'title': 'Editar membresía', 'back_url': 'membresia_list'})

def membresia_delete(request, id_membresia):
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM SGG_M_Membresia WHERE id_membresia = ?", (id_membresia,))
            messages.success(request, 'Membresía eliminada.')
            return redirect('membresia_list')
        except Exception as e:
            return render(request, 'membresia/delete.html', {
                'error': 'No se puede eliminar esta membresía porque está relacionada con otros registros.',
            })
    return render(request, 'membresia/confirm_delete.html', {'id': id_membresia})
