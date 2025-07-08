
import pydoc
import pyodbc  # ✅ Esto es lo correcto

from django.shortcuts import render
from core.services.inscripcion_service import obtener_inscripciones

from django.shortcuts import render
from core.conexion import obtener_conexion

def inscripcion_list(request):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT I.id_inscripcion, C.nombre AS cliente, TM.descripcion AS tipo_membresia,
               D.descripcion AS duracion, I.fecha_inicio, I.fecha_fin,
               I.precio_pagado, I.estado
        FROM SGG_T_Inscripcion I
        JOIN SGG_M_Cliente C ON I.id_cliente = C.id_cliente
        JOIN SGG_M_Membresia M ON I.id_membresia = M.id_membresia
        JOIN SGG_P_TipoMembresia TM ON M.id_tipo_membresia = TM.id_tipo_membresia
        JOIN SGG_P_Duracion D ON M.id_duracion = D.id_duracion
        ORDER BY I.id_inscripcion DESC
    """)
    inscripciones = cursor.fetchall()
    conn.close()

    inscripciones_data = [
        {
            'id_inscripcion': row[0],
            'cliente': row[1],
            'tipo_membresia': row[2],
            'duracion': row[3],
            'fecha_inicio': row[4],
            'fecha_fin': row[5],
            'precio_pagado': row[6],
            'estado': row[7],
        }
        for row in inscripciones
    ]

    return render(request, 'inscripcion/inscripcion_list.html', {
        'inscripciones': inscripciones_data
    })








from django.shortcuts import render, redirect
from core.forms import InscripcionForm
from core.conexion import obtener_conexion

def inscripcion_create(request):
    # Obtener clientes
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nombre FROM SGG_M_Cliente")
    clientes = cursor.fetchall()
    cliente_choices = [(str(c[0]), c[1]) for c in clientes]  # (id, nombre)

    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        form.fields['id_cliente'].choices = cliente_choices  # <- muy importante
        id_membresia = request.POST.get('id_membresia')  # viene del campo oculto (hidden input)

        if form.is_valid() and id_membresia:
            data = form.cleaned_data

            
            cursor.execute("""
                INSERT INTO SGG_T_Inscripcion (id_cliente, id_membresia, fecha_inicio, fecha_fin, precio_pagado, estado)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data['id_cliente'],
                id_membresia,
                data['fecha_inicio'],
                data['fecha_fin'],
                data['precio_pagado'],
                data['estado'],
            ))

            conn.commit()
            cursor.close()
            conn.close()
            return redirect('inscripcion_list')
    else:
        form = InscripcionForm()
        form.fields['id_cliente'].choices = cliente_choices

    # Obtener membresías (tipo + duración)
    cursor.execute("""
        SELECT M.id_membresia, TM.descripcion AS tipo, D.descripcion AS duracion
        FROM SGG_M_Membresia M
        JOIN SGG_P_TipoMembresia TM ON M.id_tipo_membresia = TM.id_tipo_membresia
        JOIN SGG_P_Duracion D ON M.id_duracion = D.id_duracion
    """)
    membresias = cursor.fetchall()
    conn.close()

    membresia_data = [
        {'id': row[0], 'tipo': row[1], 'duracion': row[2]} for row in membresias
    ]

    return render(request, 'inscripcion/inscripcion_form.html', {
        'form': form,
        'membresia_data': membresia_data,
        'is_editing': False
    })




















from django.shortcuts import render, redirect
from core.forms import InscripcionForm
from core.conexion import obtener_conexion

def inscripcion_update(request, id_inscripcion):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener clientes
    cursor.execute("SELECT id_cliente, nombre FROM SGG_M_Cliente")
    clientes = cursor.fetchall()
    cliente_choices = [(str(c[0]), c[1]) for c in clientes]

    # Obtener membresías para JS
    cursor.execute("""
        SELECT M.id_membresia, TM.descripcion AS tipo, D.descripcion AS duracion
        FROM SGG_M_Membresia M
        JOIN SGG_P_TipoMembresia TM ON M.id_tipo_membresia = TM.id_tipo_membresia
        JOIN SGG_P_Duracion D ON M.id_duracion = D.id_duracion
    """)
    membresias = cursor.fetchall()
    membresia_data = [{'id': row[0], 'tipo': row[1], 'duracion': row[2]} for row in membresias]

    # Obtener inscripción actual
    cursor.execute("""
        SELECT id_cliente, id_membresia, fecha_inicio, fecha_fin, precio_pagado, estado
        FROM SGG_T_Inscripcion
        WHERE id_inscripcion = ?
    """, (id_inscripcion,))
    inscripcion = cursor.fetchone()

    if not inscripcion:
        conn.close()
        return redirect('inscripcion_list')

    # Buscar tipo y duración actuales desde membresia_data
    tipo_actual = ''
    duracion_actual = ''
    for m in membresia_data:
        if m['id'] == inscripcion[1]:
            tipo_actual = m['tipo']
            duracion_actual = m['duracion']
            break

    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        form.fields['id_cliente'].choices = cliente_choices
        id_membresia = request.POST.get('id_membresia')

        if form.is_valid() and id_membresia:
            data = form.cleaned_data
            cursor.execute("""
                UPDATE SGG_T_Inscripcion
                SET id_cliente = ?, id_membresia = ?, fecha_inicio = ?, fecha_fin = ?, precio_pagado = ?, estado = ?
                WHERE id_inscripcion = ?
            """, (
                data['id_cliente'],
                id_membresia,
                data['fecha_inicio'],
                data['fecha_fin'],
                data['precio_pagado'],
                data['estado'],
                id_inscripcion
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('inscripcion_list')
    else:
        form = InscripcionForm(initial={
            'id_cliente': str(inscripcion[0]),
            'fecha_inicio': inscripcion[2],
            'fecha_fin': inscripcion[3],
            'precio_pagado': inscripcion[4],
            'estado': inscripcion[5],
        })
        form.fields['id_cliente'].choices = cliente_choices

    conn.close()
    return render(request, 'inscripcion/inscripcion_form.html', {
        'form': form,
        'membresia_data': membresia_data,
        'is_editing': True,
        'id_membresia_actual': inscripcion[1],
        'tipo_actual': tipo_actual,
        'duracion_actual': duracion_actual,
    })









def inscripcion_delete(request, id_inscripcion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT i.id_inscripcion, c.nombre, i.fecha_inicio, i.fecha_fin
        FROM SGG_T_Inscripcion i
        INNER JOIN SGG_M_Cliente c ON i.id_cliente = c.id_cliente
        WHERE i.id_inscripcion = ?
    """, (id_inscripcion,))
    inscripcion = cursor.fetchone()

    if not inscripcion:
        conexion.close()
        return redirect('inscripcion_list')

    id_inscripcion, nombre_cliente, fecha_inicio, fecha_fin = inscripcion

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM SGG_T_Inscripcion WHERE id_inscripcion = ?", (id_inscripcion,))
            conexion.commit()
            conexion.close()
            return redirect('inscripcion_list')
        except pyodbc.IntegrityError:
            conexion.close()
            return render(request, 'inscripcion/inscripcion_confirm_0delete.html', {
                'id_inscripcion': id_inscripcion,
                'nombre': nombre_cliente,
                'error': 'No se puede eliminar la inscripción porque tiene evaluaciones asociadas.'
            })


    conexion.close()
    return render(request, 'inscripcion/inscripcion_confirm_delete.html', {
        'id_inscripcion': id_inscripcion,
        'nombre_cliente': nombre_cliente,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin
    })
