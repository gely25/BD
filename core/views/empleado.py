
import pydoc
import pyodbc  # ✅ Esto es lo correcto

from django.shortcuts import render
from core.services.inscripcion_service import obtener_inscripciones

from django.shortcuts import render
from core.conexion import obtener_conexion

def empleado_list(request):
    q = request.GET.get('q', '').strip()
    rol_filtro = request.GET.get('rol', '').strip()
    orden_actual = request.GET.get('orden', 'id_empleado')
    direccion = request.GET.get('direccion', 'asc')

    columnas_validas = ['id_empleado', 'rol', 'nombre', 'dni', 'telefono', 'email']
    if orden_actual not in columnas_validas:
        orden_actual = 'id_empleado'
    if direccion.lower() not in ['asc', 'desc']:
        direccion = 'asc'

    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener lista de roles para filtro
    cursor.execute("SELECT id_rol, descripcion FROM SGG_P_Rol")
    roles = cursor.fetchall()

    filtros = []
    params = []

    if q:
        filtros.append("(E.nombre LIKE ? OR E.dni LIKE ? OR E.email LIKE ?)")
        like_q = f'%{q}%'
        params.extend([like_q, like_q, like_q])

    if rol_filtro:
        filtros.append("E.id_rol = ?")
        params.append(rol_filtro)

    where_sql = "WHERE " + " AND ".join(filtros) if filtros else ""

    query = f"""
        SELECT E.id_empleado, R.descripcion AS rol, E.nombre, E.dni,
               E.telefono, E.email
        FROM SGG_M_Empleado E
        JOIN SGG_P_Rol R ON E.id_rol = R.id_rol
        {where_sql}
        ORDER BY {orden_actual} {direccion.upper()}
    """

    cursor.execute(query, params)
    empleados = cursor.fetchall()
    conn.close()

    inscripciones_data = [
        {
            'id_empleado': row[0],
            'rol': row[1],
            'nombre': row[2],
            'dni': row[3],
            'telefono': row[4],
            'email': row[5],
        }
        for row in empleados
    ]

    context = {
        'inscripciones': inscripciones_data,
        'roles': roles,
        'q': q,
        'rol_filtro': rol_filtro,
        'orden_actual': orden_actual,
        'direccion': direccion,
        'columnas': [
            ('id_empleado', 'ID'),
            ('rol', 'Rol'),
            ('nombre', 'Nombre'),
            ('dni', 'DNI'),
            ('telefono', 'Teléfono'),
            ('email', 'Email'),
        ],
    }

    return render(request, 'empleado/empleado_list.html', context)








from django.shortcuts import render, redirect
from core.forms import EmpleadoForm
from core.conexion import obtener_conexion

def empleado_create(request):
    # Obtener clientes
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT id_rol, descripcion FROM SGG_P_Rol")
    clientes = cursor.fetchall()
    cliente_choices = [(str(c[0]), c[1]) for c in clientes]  # (id, nombre)

    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        form.fields['id_rol'].choices = cliente_choices  # <- muy importante# viene del campo oculto (hidden input)

        if form.is_valid():
            data = form.cleaned_data

            
            cursor.execute("""
                INSERT INTO SGG_M_Empleado (id_rol, nombre, dni, telefono, email)
                VALUES (?, ?, ?, ?, ?)
            """, (
                data['id_rol'],
                data['nombre'],
                data['dni'],
                data['telefono'],
                data['email'],
            ))

            conn.commit()
            cursor.close()
            conn.close()
            return redirect('empleado_list')
    else:
        form = EmpleadoForm()
        form.fields['id_rol'].choices = cliente_choices

    # Obtener membresías (tipo + duración)

    return render(request, 'empleado/empleado_form.html', {
        'form': form,
        'is_editing': False
    })




















from django.shortcuts import render, redirect
from core.forms import EmpleadoForm
from core.conexion import obtener_conexion

def empleado_update(request, id_empleado):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener clientes
    cursor.execute("SELECT id_rol, descripcion FROM SGG_P_Rol")
    clientes = cursor.fetchall()
    cliente_choices = [(str(c[0]), c[1]) for c in clientes]

    # Obtener membresías para JS

    # Obtener inscripción actual
    cursor.execute("""
        SELECT id_rol, nombre, dni, telefono, email
        FROM SGG_M_Empleado
        WHERE id_empleado = ?
    """, (id_empleado,))
    inscripcion = cursor.fetchone()

    if not inscripcion:
        conn.close()
        return redirect('empleado_list')

    # Buscar tipo y duración actuales desde membresia_data

    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        form.fields['id_rol'].choices = cliente_choices

        if form.is_valid() :
            data = form.cleaned_data
            cursor.execute("""
                UPDATE SGG_M_Empleado
                SET id_rol = ?, nombre = ?, dni = ?, telefono = ?, email = ?
                WHERE id_empleado = ?
            """, (
                data['id_rol'],
                data['nombre'],
                data['dni'],
                data['telefono'],
                data['email'],
                id_empleado
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('empleado_list')
    else:
        form = EmpleadoForm(initial={
            'id_rol': str(inscripcion[0]),
            'nombre': inscripcion[1],
            'dni': inscripcion[2],
            'telefono': inscripcion[3],
            'email': inscripcion[4],
        })
        form.fields['id_rol'].choices = cliente_choices

    conn.close()
    return render(request, 'empleado/empleado_form.html', {
        'form': form,
        'is_editing': True,
    })









def empleado_delete(request, id_empleado):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT E.id_empleado, r.descripcion, E.nombre, E.dni, E.telefono, E.email
        FROM SGG_M_Empleado E
        INNER JOIN SGG_P_Rol r ON E.id_rol = r.id_rol
        WHERE E.id_empleado = ?
    """, (id_empleado,))
    inscripcion = cursor.fetchone()

    if not inscripcion:
        conexion.close()
        return redirect('empleado_list')

    id_empleado, nombre_cliente, nombre, dni,telefono, email = inscripcion

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM SGG_M_Empleado WHERE id_empleado = ?", (id_empleado,))
            conexion.commit()
            conexion.close()
            return redirect('empleado_list')
        except pyodbc.IntegrityError:
            conexion.close()
            return render(request, 'empleado/empleado_confirm_delete.html', {
                'id_inscripcion': id_empleado,
                'nombre': nombre_cliente,
                'error': 'No se puede eliminar la inscripción porque tiene evaluaciones asociadas.'
            })


    conexion.close()
    return render(request, 'empleado/empleado_confirm_delete.html', {
        'id_inscripcion': id_empleado,
        'nombre_cliente': nombre_cliente,
        'fecha_inicio': dni,
        'telefono': telefono,
        "email": email
    })