
from django.shortcuts import render, redirect
from core.conexion import obtener_conexion

def seguimiento_rutina_list(request):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener parámetros de búsqueda y ordenamiento
    search_query = request.GET.get('search', '').strip()
    order_by = request.GET.get('order_by', 'id_rutina')
    order_direction = request.GET.get('order_direction', 'asc')

    # Validar campos permitidos para evitar inyección SQL
    allowed_order_fields = ['id_rutina', 'dia_semana', 'nombre_cliente']
    if order_by not in allowed_order_fields:
        order_by = 'id_rutina'

    # Validar dirección de ordenamiento
    if order_direction not in ['asc', 'desc']:
        order_direction = 'asc'

    # Construir la consulta SQL con parámetros
    query = f"""
        SELECT sr.id_seguimiento, sr.id_rutina, sr.dia_semana, sr.fecha_programada, sr.estado_cumplimiento, c.nombre
        FROM SGG_T_SeguimientoRutina sr
        JOIN SGG_T_Rutina r ON sr.id_rutina = r.id_rutina
        JOIN SGG_T_Inscripcion i ON r.id_evaluacion = i.id_inscripcion
        JOIN SGG_M_Cliente c ON i.id_cliente = c.id_cliente
        WHERE LOWER(c.nombre) LIKE ?
        ORDER BY {order_by} {order_direction}
    """
    params = [f'%{search_query.lower()}%'] if len(search_query) >= 3 else ['%']

    try:
        # Ejecutar la consulta
        cursor.execute(query, params)
        seguimientos = cursor.fetchall()
    except Exception as e:
        print(f"Error al ejecutar la consulta: {e}")
        seguimientos = []

    conn.close()

    seguimientos_data = [
        {
            'id_seguimiento': row[0],
            'id_rutina': row[1],
            'dia_semana': row[2],
            'fecha_programada': row[3],
            'estado_cumplimiento': row[4],
            'nombre_cliente': row[5],
        }
        for row in seguimientos
    ]

    return render(request, 'seguimiento_rutina/seguimiento_rutina_list.html', {
        'seguimientos': seguimientos_data,
        'search_query': search_query,
        'order_by': order_by,
        'order_direction': order_direction
    })


from django.shortcuts import render, redirect
from core.forms import SeguimientoRutinaForm
from core.conexion import obtener_conexion

def seguimiento_rutina_create(request):
    if request.method == 'POST':
        form = SeguimientoRutinaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO SGG_T_SeguimientoRutina (id_rutina, dia_semana, fecha_programada, estado_cumplimiento)
                VALUES (?, ?, ?, ?)
            """, (
                data['id_rutina'],
                data['dia_semana'],
                data['fecha_programada'],
                data['estado_cumplimiento']
            ))
            conn.commit()
            conn.close()
            return redirect('seguimiento_rutina_list')
    else:
        form = SeguimientoRutinaForm()
    return render(request, 'seguimiento_rutina/seguimiento_rutina_form.html', {'form': form, 'is_editing': False})


from django.shortcuts import render, redirect
from core.forms import SeguimientoRutinaForm
from core.conexion import obtener_conexion

def seguimiento_rutina_update(request, id_seguimiento):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_rutina, dia_semana, fecha_programada, estado_cumplimiento
        FROM SGG_T_SeguimientoRutina
        WHERE id_seguimiento = ?
    """, (id_seguimiento,))
    seguimiento = cursor.fetchone()

    if not seguimiento:
        conn.close()
        return redirect('seguimiento_rutina_list')

    if request.method == 'POST':
        form = SeguimientoRutinaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cursor.execute("""
                UPDATE SGG_T_SeguimientoRutina
                SET id_rutina = ?, dia_semana = ?, fecha_programada = ?, estado_cumplimiento = ?
                WHERE id_seguimiento = ?
            """, (
                data['id_rutina'],
                data['dia_semana'],
                data['fecha_programada'],
                data['estado_cumplimiento'],
                id_seguimiento
            ))
            conn.commit()
            conn.close()
            return redirect('seguimiento_rutina_list')
    else:
        form = SeguimientoRutinaForm(initial={
            'id_rutina': seguimiento[0],
            'dia_semana': seguimiento[1],
            'fecha_programada': seguimiento[2],
            'estado_cumplimiento': seguimiento[3],
        })

    conn.close()
    return render(request, 'seguimiento_rutina/seguimiento_rutina_form.html', {'form': form, 'is_editing': True})



from django.shortcuts import render, redirect
from core.conexion import obtener_conexion

def seguimiento_rutina_delete(request, id_seguimiento):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT dia_semana
        FROM SGG_T_SeguimientoRutina
        WHERE id_seguimiento = ?
    """, (id_seguimiento,))
    seguimiento = cursor.fetchone()

    if not seguimiento:
        conn.close()
        return redirect('seguimiento_rutina_list')

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM SGG_T_SeguimientoRutina WHERE id_seguimiento = ?", (id_seguimiento,))
            conn.commit()
            conn.close()
            return redirect('seguimiento_rutina_list')
        except Exception as e:
            conn.close()
            return render(request, 'seguimiento_rutina/seguimiento_rutina_confirm_delete.html', {
                'id_seguimiento': id_seguimiento,
                'dia_semana': seguimiento[0],
                'error': 'No se puede eliminar este seguimiento porque está relacionado con otros registros.'
            })

    conn.close()
    return render(request, 'seguimiento_rutina/delete.html', {
        'id_seguimiento': id_seguimiento,
        'dia_semana': seguimiento[0]
    })