from django.http import HttpResponse
import pyodbc
from django.shortcuts import render, redirect
from core.conexion import obtener_conexion
from core.forms import RolForm
from core.services.rol_service import obtener_roles

def rol_list(request):
    condiciones = obtener_roles()
    return render(request, 'rol/rol_list.html', {'condiciones': condiciones})

def rol_create(request):
    if request.method == 'POST':
        print("📩 Formulario recibido (POST)")
        print("Datos POST:", request.POST)

        form = RolForm(request.POST)
        print("¿Formulario válido?:", form.is_valid())

        if form.is_valid():
            data = form.cleaned_data
            print("✅ Datos limpios:", data)

            try:
                # Conexión a SQL Server
              
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=LAPTOP-HB6P5DN7;'  # corregido
                    'DATABASE=SGG;'
                    'Trusted_Connection=yes;'
                )

                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO SGG_P_Rol (descripcion)
                    VALUES (?)
                """, (
                    data["descripcion"],
                ))

                conn.commit()
                cursor.close()
                conn.close()

                print("🎉 Condicion guardado correctamente.")
                return redirect('rol_list')

            except Exception as e:
                print("❌ Error al guardar en BD:", str(e))
                form.add_error(None, f"Error al guardar: {e}")
        else:
            print("⚠️ Errores del formulario:", form.errors)

    else:
        print("📄 Mostrando formulario vacío (GET)")
        form = RolForm()

    return render(request, 'rol/rol_form.html', {
        'form': form,
        'is_editing': False
    })

def rol_delete(request, id_rol):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtenemos el rol por ID
    cursor.execute("SELECT descripcion FROM SGG_P_Rol WHERE id_rol = ?", (id_rol,))
    rol = cursor.fetchone()

    if not rol:
        conexion.close()
        return redirect('rol_list')  # Si no existe, volvemos

    nombre_rol = rol[0]

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM SGG_P_Rol WHERE id_rol = ?", (id_rol,))
            conexion.commit()
            conexion.close()
            return redirect('rol_list')
        except pyodbc.IntegrityError:
            conexion.close()
            return render(request, 'rol/delete.html', {
                'id_rol': id_rol,
                'nombre': nombre_rol,
                'error': 'No se puede eliminar el rol porque está siendo utilizado.'
            })

    conexion.close()
    return render(request, 'rol/delete.html', {
        'id_rol': id_rol,
        'nombre': nombre_rol
    })


def rol_update(request, id_cliente):
    # DEBUG: Imprimir información
    print(f"🔍 DEBUGGING cliente_update:")
    print(f"   - id_cliente recibido: {id_cliente}")
    print(f"   - Tipo de id_cliente: {type(id_cliente)}")
    print(f"   - Método de request: {request.method}")
    
    try:
        # Conectar con SQL Server
        conn = obtener_conexion()
        cursor = conn.cursor()
        
        print(f"   - Conexión establecida exitosamente")

        # Buscar cliente
        query = "SELECT descripcion FROM SGG_P_Rol WHERE id_rol = ?"
        print(f"   - Ejecutando query: {query}")
        print(f"   - Con parámetro: {id_cliente}")
        
        cursor.execute(query, (id_cliente,))
        row = cursor.fetchone()
        
        print(f"   - Resultado de la query: {row}")

        if not row:
            print(f"   - ❌ Cliente no encontrado con ID: {id_cliente}")
            cursor.close()
            conn.close()
            return HttpResponse(f"Cliente con ID {id_cliente} no encontrado", status=404)

        # Desempaquetar los datos
        descripcion = row[0]
        print(f"   - ✅ Cliente encontrado: {descripcion}")

        cliente_actual = {
            'descripcion': descripcion,
        }
        
        print(f"   - Datos del cliente: {cliente_actual}")

        if request.method == 'POST':
            print(f"   - Procesando POST")
            form = RolForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(f"   - Datos del formulario válidos: {data}")
                
                cursor.execute("""
                    UPDATE SGG_P_Rol
                    SET descripcion = ?
                    WHERE id_rol = ?
                """, (
                    data['descripcion'],
                    id_cliente
                ))
                conn.commit()
                print(f"   - ✅ Cliente actualizado exitosamente")
                cursor.close()
                conn.close()
                return redirect('rol_list')
            else:
                print(f"   - ❌ Errores en el formulario: {form.errors}")
        else:
            print(f"   - Mostrando formulario GET")
            form = RolForm(initial=cliente_actual)

        cursor.close()
        conn.close()

        print(f"   - Renderizando template con is_editing=True")
        return render(request, 'rol/rol_form.html', {
            'form': form,
            'is_editing': True,
            'id_condicion_fisica': id_cliente,
        })

    except Exception as e:
        print(f"   - ❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
        
        return render(request, 'rol/rol_form.html', {
            'form': RolForm(),
            'error': f"Ocurrió un error: {e}",
            'is_editing': False,
        })