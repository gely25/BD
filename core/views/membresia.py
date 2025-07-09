from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.forms import MembresiaForm
from core.models import SggMMembresia
import pyodbc
from django.db import connection

import pyodbc
from django.core.paginator import Paginator
from django.shortcuts import render
from django.conf import settings



def membresia_update(request, id_membresia):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Buscar la membresía manualmente
    cursor.execute("""
        SELECT id_tipo_membresia, id_duracion, precio_actual, descripcion
        FROM SGG_M_Membresia
        WHERE id_membresia = ?
    """, (id_membresia,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return render(request, '404.html', status=404)  # o tu propia vista de error

    if request.method == 'POST':
        form = MembresiaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cursor.execute("""
                UPDATE SGG_M_Membresia
                SET id_tipo_membresia = ?, id_duracion = ?, precio_actual = ?, descripcion = ?
                WHERE id_membresia = ?
            """, (
                data['id_tipo_membresia'],
                data['id_duracion'],
                data['precio_actual'],
                data['descripcion'],
                id_membresia
            ))
            conn.commit()
            conn.close()
            messages.success(request, 'Membresía actualizada.')
            return redirect('membresia_list')
    else:
        form = MembresiaForm(initial={
            'id_tipo_membresia': row[0],
            'id_duracion': row[1],
            'precio_actual': row[2],
            'descripcion': row[3],
        })

    conn.close()
    return render(request, 'membresia/form.html', {
        'form': form,
        'title': 'Editar membresía',
        'back_url': 'membresia_list'
    })






import pyodbc
from django.shortcuts import render, redirect
from django.contrib import messages
from core.forms import MembresiaForm
from core.conexion import obtener_conexion


def membresia_create(request):
    if request.method == 'POST':
        form = MembresiaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Conexión directa a SQL Server
            conn = obtener_conexion()
            cursor = conn.cursor()

            sql = """
                INSERT INTO SGG_M_Membresia (id_tipo_membresia, id_duracion, precio_actual, descripcion)
                VALUES (?, ?, ?, ?)
            """
            valores = (
                data['id_tipo_membresia'],
                data['id_duracion'],
                data['precio_actual'],
                data['descripcion']
            )

            cursor.execute(sql, valores)
            conn.commit()
            conn.close()

            messages.success(request, 'Membresía registrada exitosamente.')
            return redirect('membresia_list')
    else:
        form = MembresiaForm()

    return render(request, 'membresia/form.html', {
        'form': form,
        'title': 'Registrar membresía',
        'back_url': 'membresia_list'
    })




def membresia_delete(request, id_membresia):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener nombre o descripción para mostrar
    cursor.execute("SELECT descripcion FROM SGG_M_Membresia WHERE id_membresia = ?", (id_membresia,))
    row = cursor.fetchone()
    nombre_membresia = row[0] if row else 'Membresía desconocida'

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM SGG_M_Membresia WHERE id_membresia = ?", (id_membresia,))
            conn.commit()
            conn.close()
            messages.success(request, 'Membresía eliminada.')
            return redirect('membresia_list')
        except Exception as e:
            conn.close()
            return render(request, 'membresia/confirm_delete.html', {
                'id': id_membresia,
                'nombre_membresia': nombre_membresia,
                'error': 'No se puede eliminar esta membresía porque está relacionada con otros registros.'
            })

    conn.close()
    return render(request, 'membresia/confirm_delete.html', {
        'id': id_membresia,
        'nombre_membresia': nombre_membresia
    })






# views.py - Versión simplificada y funcional
from django.core.paginator import Paginator
from django.shortcuts import render

def membresia_list(request):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Filtros desde GET
    query = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '')
    duracion = request.GET.get('duracion', '')
    precio_op = request.GET.get("precio_op", '')
    precio_valor = request.GET.get("precio_valor", '')
    
    # Ordenamiento simple
    sort = request.GET.get('sort', '0')
    desc = request.GET.get('desc', '0')

    # SQL base
    sql = """
        SELECT 
            m.id_membresia,
            tm.descripcion AS tipo_membresia,
            d.descripcion AS duracion,
            m.precio_actual,
            m.descripcion,
            m.id_tipo_membresia,
            m.id_duracion
        FROM 
            SGG_M_Membresia m
        JOIN 
            SGG_P_TipoMembresia tm ON m.id_tipo_membresia = tm.id_tipo_membresia
        JOIN 
            SGG_P_Duracion d ON m.id_duracion = d.id_duracion
    """

    condiciones = []
    params = []

    # Aplicar filtros
    if query:
        condiciones.append("""
            (tm.descripcion LIKE ? OR 
             d.descripcion LIKE ? OR 
             m.descripcion LIKE ?)
        """)
        params += [f'%{query}%'] * 3

    if tipo:
        condiciones.append("m.id_tipo_membresia = ?")
        params.append(tipo)

    if duracion:
        condiciones.append("m.id_duracion = ?")
        params.append(duracion)

    # Filtro por precio
    if precio_op and precio_valor:
        try:
            valor = float(precio_valor)
            if precio_op == "lt":
                condiciones.append("m.precio_actual < ?")
                params.append(valor)
            elif precio_op == "gt":
                condiciones.append("m.precio_actual > ?")
                params.append(valor)
            elif precio_op == "eq":
                condiciones.append("m.precio_actual = ?")
                params.append(valor)
        except ValueError:
            pass

    # Aplicar condiciones WHERE
    if condiciones:
        sql += " WHERE " + " AND ".join(condiciones)

    # Ordenamiento simple
    column_map = {
        '0': 'm.id_membresia',
        '1': 'tm.descripcion',
        '2': 'd.descripcion',
        '3': 'm.precio_actual',
        '4': 'm.descripcion',
    }
    
    if sort in column_map:
        direction = 'DESC' if desc == '1' else 'ASC'
        sql += f" ORDER BY {column_map[sort]} {direction}"

    print("SQL Query:", sql)  # Debug
    print("Params:", params)  # Debug

    # Ejecutar consulta
    cursor.execute(sql, params)
    rows = cursor.fetchall()

    print("Rows found:", len(rows))  # Debug

    # Paginación
    paginator = Paginator(rows, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Opciones para filtros
    cursor.execute("SELECT id_tipo_membresia, descripcion FROM SGG_P_TipoMembresia ORDER BY descripcion")
    tipos = [{'id': row[0], 'descripcion': row[1]} for row in cursor.fetchall()]

    cursor.execute("SELECT id_duracion, descripcion FROM SGG_P_Duracion ORDER BY descripcion")
    duraciones = [{'id': row[0], 'descripcion': row[1]} for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    context = {
        "page_obj": page_obj,
        "query": query,
        "tipo": tipo,
        "duracion": duracion,
        "tipos": tipos,
        "duraciones": duraciones,
        "precio_op": precio_op,
        "precio_valor": precio_valor,
        "sort": sort,
        "desc": desc,
    }

    return render(request, "membresia/list.html", context)