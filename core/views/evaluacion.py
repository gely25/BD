
import pydoc
import pyodbc  # ✅ Esto es lo correcto

from django.shortcuts import render
from core.services.inscripcion_service import obtener_inscripciones

from django.shortcuts import render
from core.conexion import obtener_conexion

def evaluacion_list(request):
    q = request.GET.get('q', '').strip()
    condicion_filtro = request.GET.get('condicion', '').strip()
    fecha_desde = request.GET.get('fecha_desde', '').strip()
    fecha_hasta = request.GET.get('fecha_hasta', '').strip()
    orden_actual = request.GET.get('orden', 'id_evaluacion')
    direccion = request.GET.get('direccion', 'asc')

    columnas_validas = [
        'id_evaluacion', 'inscripcion', 'empleado',
        'peso', 'altura', 'fecha', 'grasa_corporal',
        'presion_arterial', 'condicion'
    ]

    if orden_actual not in columnas_validas:
        orden_actual = 'id_evaluacion'
    if direccion.lower() not in ['asc', 'desc']:
        direccion = 'asc'

    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT descripcion FROM SGG_P_CondicionFIsica")
    condiciones = [row[0] for row in cursor.fetchall()]

    filtros = []
    params = []

    if q:
        filtros.append("(cl.nombre LIKE ? OR em.nombre LIKE ?)")
        params.extend([f'%{q}%', f'%{q}%'])

    if condicion_filtro:
        filtros.append("c.descripcion = ?")
        params.append(condicion_filtro)

    if fecha_desde:
        filtros.append("E.fecha >= ?")
        params.append(fecha_desde)

    if fecha_hasta:
        filtros.append("E.fecha <= ?")
        params.append(fecha_hasta)

    where_sql = "WHERE " + " AND ".join(filtros) if filtros else ""

    query = f"""
        SELECT 
            E.id_evaluacion, 
            cl.nombre AS inscripcion,
            em.nombre AS empleado,
            E.peso,
            E.altura,
            E.fecha,
            E.grasa_corporal,
            E.presion_arterial,
            c.descripcion AS condicion
        FROM SGG_T_EvaluacionFisica E
        JOIN SGG_T_Inscripcion I ON E.id_inscripcion = I.id_inscripcion
        JOIN SGG_M_Empleado em ON E.id_empleado = em.id_empleado
        JOIN SGG_P_CondicionFIsica c ON E.id_condicion_fisica = c.id_condicion_fisica
        JOIN SGG_M_Cliente cl ON I.id_cliente = cl.id_cliente
        {where_sql}
        ORDER BY {orden_actual} {direccion.upper()}
    """

    cursor.execute(query, params)
    filas = cursor.fetchall()
    conn.close()

    inscripciones_data = [
        {
            'id_evaluacion': row[0],
            'inscripcion': row[1],
            'empleado': row[2],
            'peso': row[3],
            'altura': row[4],
            'fecha': row[5],
            'grasa_corporal': row[6],
            'presion_arterial': row[7],
            'condicion': row[8],
        }
        for row in filas
    ]

    columnas = [
        ('id_evaluacion', 'ID'),
        ('inscripcion', 'Cliente'),
        ('empleado', 'Empleado'),
        ('peso', 'Peso'),
        ('altura', 'Altura'),
        ('fecha', 'Fecha'),
        ('grasa_corporal', 'Grasa Corporal'),
        ('presion_arterial', 'Presión Arterial'),
        ('condicion', 'Condición Física'),
    ]

    context = {
        'inscripciones': inscripciones_data,
        'condiciones': condiciones,
        'q': q,
        'condicion_filtro': condicion_filtro,
        'fecha_desde': fecha_desde,
        'fecha_hasta': fecha_hasta,
        'orden_actual': orden_actual,
        'direccion': direccion,
        'columnas': columnas,
    }
    return render(request, 'evaluacion fisica/evaluacion_list.html', context)








from django.shortcuts import render, redirect
from core.forms import EvaluacionForm
from core.conexion import obtener_conexion

def evaluacion_create(request):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener inscripciones con nombre del cliente
    cursor.execute("""
        SELECT I.id_inscripcion, C.nombre 
        FROM SGG_T_Inscripcion I
        JOIN SGG_M_Cliente C ON I.id_cliente = C.id_cliente
    """)
    inscripciones = [(str(row[0]), row[1]) for row in cursor.fetchall()]

    # Obtener empleados
    cursor.execute("SELECT id_empleado, nombre FROM SGG_M_Empleado")
    empleados = [(str(row[0]), row[1]) for row in cursor.fetchall()]

    # Obtener condiciones físicas
    cursor.execute("SELECT id_condicion_fisica, descripcion FROM SGG_P_CondicionFisica")
    condiciones = [(str(row[0]), row[1]) for row in cursor.fetchall()]

    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        form.fields['id_inscripcion'].choices = inscripciones
        form.fields['id_empleado'].choices = empleados
        form.fields['id_condicion_fisica'].choices = condiciones

        if form.is_valid():
            data = form.cleaned_data
            cursor.execute("""
                INSERT INTO SGG_T_EvaluacionFisica (
                    id_inscripcion, id_empleado, peso, altura, fecha,
                    grasa_corporal, presion_arterial, id_condicion_fisica
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data['id_inscripcion'],
                data['id_empleado'],
                data['peso'],
                data['altura'],
                data['fecha'],
                data['grasa_corporal'],
                data['presion_arterial'],
                data['id_condicion_fisica'],
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('evaluacion_list')
    else:
        form = EvaluacionForm()
        form.fields['id_inscripcion'].choices = inscripciones
        form.fields['id_empleado'].choices = empleados
        form.fields['id_condicion_fisica'].choices = condiciones

    conn.close()
    return render(request, 'evaluacion fisica/evaluacion_form.html', {
        'form': form,
        'is_editing': False
    })




















from django.shortcuts import render, redirect
from core.forms import EmpleadoForm
from core.conexion import obtener_conexion

def evaluacion_update(request, id_evaluacion):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener inscripciones (cliente)
    cursor.execute("""
        SELECT I.id_inscripcion, C.nombre
        FROM SGG_T_Inscripcion I
        JOIN SGG_M_Cliente C ON I.id_cliente = C.id_cliente
    """)
    inscripciones = [(str(row[0]), row[1]) for row in cursor.fetchall()]

    # Obtener empleados
    cursor.execute("SELECT id_empleado, nombre FROM SGG_M_Empleado")
    empleados = [(str(row[0]), row[1]) for row in cursor.fetchall()]

    # Obtener condiciones físicas
    cursor.execute("SELECT id_condicion_fisica, descripcion FROM SGG_P_CondicionFisica")
    condiciones = [(str(row[0]), row[1]) for row in cursor.fetchall()]

    # Obtener evaluación actual
    cursor.execute("""
        SELECT id_inscripcion, id_empleado, peso, altura, fecha, grasa_corporal, presion_arterial, id_condicion_fisica
        FROM SGG_T_EvaluacionFisica
        WHERE id_evaluacion = ?
    """, (id_evaluacion,))
    evaluacion = cursor.fetchone()

    if not evaluacion:
        cursor.close()
        conn.close()
        return redirect('evaluacion_list')

    if request.method == 'POST':
        form = EvaluacionForm(request.POST)
        form.fields['id_inscripcion'].choices = inscripciones
        form.fields['id_empleado'].choices = empleados
        form.fields['id_condicion_fisica'].choices = condiciones

        if form.is_valid():
            data = form.cleaned_data
            cursor.execute("""
                UPDATE SGG_T_EvaluacionFisica
                SET id_inscripcion = ?, id_empleado = ?, peso = ?, altura = ?, fecha = ?,
                    grasa_corporal = ?, presion_arterial = ?, id_condicion_fisica = ?
                WHERE id_evaluacion = ?
            """, (
                data['id_inscripcion'],
                data['id_empleado'],
                data['peso'],
                data['altura'],
                data['fecha'],
                data['grasa_corporal'],
                data['presion_arterial'],
                data['id_condicion_fisica'],
                id_evaluacion
            ))
            conn.commit()
            cursor.close()
            conn.close()
            return redirect('evaluacion_list')
    else:
        form = EvaluacionForm(initial={
            'id_inscripcion': str(evaluacion[0]),
            'id_empleado': str(evaluacion[1]),
            'peso': evaluacion[2],
            'altura': evaluacion[3],
            'fecha': evaluacion[4],
            'grasa_corporal': evaluacion[5],
            'presion_arterial': evaluacion[6],
            'id_condicion_fisica': str(evaluacion[7]),
        })
        form.fields['id_inscripcion'].choices = inscripciones
        form.fields['id_empleado'].choices = empleados
        form.fields['id_condicion_fisica'].choices = condiciones

    cursor.close()
    conn.close()
    return render(request, 'evaluacion fisica/evaluacion_form.html', {
        'form': form,
        'is_editing': True
    })









def evaluacion_delete(request, id_evaluacion):
    conn = obtener_conexion()
    cursor = conn.cursor()

    # Obtener datos de la evaluación para mostrar al usuario
    cursor.execute("""
        SELECT E.id_evaluacion, C.nombre, EM.nombre, E.fecha, E.peso, E.altura
        FROM SGG_T_EvaluacionFisica E
        JOIN SGG_T_Inscripcion I ON E.id_inscripcion = I.id_inscripcion
        JOIN SGG_M_Cliente C ON I.id_cliente = C.id_cliente
        JOIN SGG_M_Empleado EM ON E.id_empleado = EM.id_empleado
        WHERE E.id_evaluacion = ?
    """, (id_evaluacion,))
    evaluacion = cursor.fetchone()

    if not evaluacion:
        conn.close()
        return redirect('evaluacion_list')

    id_evaluacion, nombre_cliente, nombre_empleado, fecha, peso, altura = evaluacion

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM SGG_T_EvaluacionFisica WHERE id_evaluacion = ?", (id_evaluacion,))
            conn.commit()
            conn.close()
            return redirect('evaluacion_list')
        except pyodbc.IntegrityError:
            conn.close()
            return render(request, 'evaluacion fisica/evaluacion_confirm_delete.html', {
                'id_evaluacion': id_evaluacion,
                'nombre_cliente': nombre_cliente,
                'error': 'No se puede eliminar la evaluación porque está vinculada a otros registros.'
            })

    conn.close()
    return render(request, 'evaluacion fisica/evaluacion_confirm_delete.html', {
        'id_evaluacion': id_evaluacion,
        'nombre_cliente': nombre_cliente,
        'nombre_empleado': nombre_empleado,
        'fecha': fecha,
        'peso': peso,
        'altura': altura
    })