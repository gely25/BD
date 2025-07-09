
# core/views/tipo_membresia_views.py
from django.shortcuts import render
from core.conexion import obtener_conexion

def tipo_membresia_list(request):
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("SELECT id_tipo_membresia, descripcion FROM SGG_P_TipoMembresia")
    resultados = cursor.fetchall()

    tipos = []
    for row in resultados:
        tipos.append({
            'id_tipo_membresia': row[0],
            'descripcion': row[1],
        })

    conn.close()
    return render(request, 'tipo_membresia/list.html', {'tipos': tipos})














from django.shortcuts import render, redirect
from core.forms import TipoMembresiaForm
from core.conexion import obtener_conexion

def tipo_membresia_create(request):
    if request.method == 'POST':
        form = TipoMembresiaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            conn = obtener_conexion()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO SGG_P_TipoMembresia (descripcion)
                VALUES (?)
            """, (data['descripcion'],))
            conn.commit()
            conn.close()
            return redirect('tipo_membresia_list')
    else:
        form = TipoMembresiaForm()
    return render(request, 'tipo_membresia/form.html', {'form': form, 'is_editing': False})









def tipo_membresia_update(request, id_tipo_membresia):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT descripcion FROM SGG_P_TipoMembresia WHERE id_tipo_membresia = ?", (id_tipo_membresia,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return redirect('tipo_membresia_list')

    if request.method == 'POST':
        form = TipoMembresiaForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            cursor.execute("""
                UPDATE SGG_P_TipoMembresia SET descripcion = ?
                WHERE id_tipo_membresia = ?
            """, (data['descripcion'], id_tipo_membresia))
            conn.commit()
            conn.close()
            return redirect('tipo_membresia_list')
    else:
        form = TipoMembresiaForm(initial={'descripcion': row[0]})
    conn.close()
    return render(request, 'tipo_membresia/form.html', {
        'form': form,
        'is_editing': True,
        'id_tipo_membresia': id_tipo_membresia
    })









def tipo_membresia_delete(request, id_tipo_membresia):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT descripcion FROM SGG_P_TipoMembresia WHERE id_tipo_membresia = ?", (id_tipo_membresia,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return redirect('tipo_membresia_list')

    if request.method == 'POST':
        cursor.execute("DELETE FROM SGG_P_TipoMembresia WHERE id_tipo_membresia = ?", (id_tipo_membresia,))
        conn.commit()
        conn.close()
        return redirect('tipo_membresia_list')

    conn.close()
    return render(request, 'tipo_membresia/delete.html', {
        'id_tipo_membresia': id_tipo_membresia,
        'descripcion': row[0],
    })
