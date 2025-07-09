from django.shortcuts import render, redirect
from django.contrib import messages
from core.conexion import obtener_conexion


def rutina_list(request):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener parámetros de búsqueda y ordenamiento
    search_query = request.GET.get('search', '')
    order_by = request.GET.get('order_by', 'id_rutina')
    order_direction = request.GET.get('order_direction', 'asc')

    # Validar campos permitidos para evitar inyección SQL
    allowed_order_fields = ['id_rutina', 'nombre_rutina', 'nivel']
    if order_by not in allowed_order_fields:
        order_by = 'id_rutina'

    # Validar dirección de ordenamiento
    if order_direction not in ['asc', 'desc']:
        order_direction = 'asc'

    # Consulta con filtrado y ordenamiento
    query = f"""
        SELECT r.id_rutina, c.nombre, r.nombre_rutina, r.nivel, r.descripcion, r.objetivo
        FROM SGG_T_Rutina r
        JOIN SGG_T_Inscripcion i ON r.id_evaluacion = i.id_inscripcion
        JOIN SGG_M_Cliente c ON i.id_cliente = c.id_cliente
        WHERE r.nombre_rutina LIKE ? OR r.id_rutina LIKE ? OR r.nivel LIKE ?
        ORDER BY {order_by} {order_direction}
    """
    cursor.execute(query, (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
    rutinas = cursor.fetchall()
    conn.close()

    rutinas_data = [
        {
            'id_rutina': row[0],
            'nombre_cliente': row[1],
            'nombre_rutina': row[2],
            'nivel': row[3],
            'descripcion': row[4],
            'objetivo': row[5],
        }
        for row in rutinas
    ]

    return render(request, 'rutina/rutina_list.html', {
        'rutinas': rutinas_data,
        'search_query': search_query,
        'order_by': order_by,
        'order_direction': order_direction
    })



from django.shortcuts import render, redirect
from core.forms import RutinaForm
from core.conexion import obtener_conexion

def rutina_create(request):
    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO SGG_T_Rutina (id_evaluacion, nombre_rutina, nivel, descripcion, objetivo)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data['id_evaluacion'],
                data['nombre_rutina'],
                data['nivel'],
                data['descripcion'],
                data['objetivo']
            ))
            conn.commit()
            conn.close()
            messages.success(request, 'Rutina creada exitosamente.')
            return redirect('rutina_list')
    else:
        form = RutinaForm()
    return render(request, 'rutina/rutina_form.html', {'form': form, 'is_editing': False})

from django.shortcuts import render, redirect
from core.forms import RutinaForm
from core.conexion import obtener_conexion

def rutina_update(request, id_rutina):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_evaluacion, nombre_rutina, nivel, descripcion, objetivo
        FROM SGG_T_Rutina
        WHERE id_rutina = ?
    """, (id_rutina,))
    rutina = cursor.fetchone()

    if not rutina:
        conn.close()
        return redirect('rutina_list')

    if request.method == 'POST':
        form = RutinaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cursor.execute("""
                UPDATE SGG_T_Rutina
                SET id_evaluacion = ?, nombre_rutina = ?, nivel = ?, descripcion = ?, objetivo = ?
                WHERE id_rutina = ?
            """, (
                data['id_evaluacion'],
                data['nombre_rutina'],
                data['nivel'],
                data['descripcion'],
                data['objetivo'],
                id_rutina
            ))
            conn.commit()
            conn.close()
            messages.success(request, 'Rutina actualizada.')
            return redirect('rutina_list')
    else:
        form = RutinaForm(initial={
            'id_evaluacion': rutina[0],
            'nombre_rutina': rutina[1],
            'nivel': rutina[2],
            'descripcion': rutina[3],
            'objetivo': rutina[4],
        })

    conn.close()
    return render(request, 'rutina/rutina_form.html', {'form': form, 'is_editing': True})



from django.shortcuts import render, redirect
from core.conexion import obtener_conexion

def rutina_delete(request, id_rutina):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT nombre_rutina
        FROM SGG_T_Rutina
        WHERE id_rutina = ?
    """, (id_rutina,))
    rutina = cursor.fetchone()

    if not rutina:
        conn.close()
        return redirect('rutina_list')

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM SGG_T_Rutina WHERE id_rutina = ?", (id_rutina,))
            conn.commit()
            conn.close()
            messages.success(request, 'Rutina eliminada.')
            return redirect('rutina_list')
        except Exception as e:
            conn.close()
            return render(request, 'rutina/rutina_confirm_delete.html', {
                'id_rutina': id_rutina,
                'nombre_rutina': rutina[0],
                'error': 'No se puede eliminar esta rutina porque está relacionada con otros registros.'
            })

    conn.close()
    return render(request, 'rutina/rutina_confirm_delete.html', {
        'id_rutina': id_rutina,
        'nombre_rutina': rutina[0]
    })