from django.http import HttpResponse
import pyodbc
from django.shortcuts import render, redirect
from core.conexion import obtener_conexion
from core.forms import CondicionForm
from core.services.condicion_service import obtener_condiciones

def condicion_list(request):
    condiciones = obtener_condiciones()
    return render(request, 'condicion fisica/condicion_list.html', {'condiciones': condiciones})

def condicion_create(request):
    if request.method == 'POST':
        print("📩 Formulario recibido (POST)")
        print("Datos POST:", request.POST)

        form = CondicionForm(request.POST)
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
                    INSERT INTO SGG_P_CondicionFisica (descripcion)
                    VALUES (?)
                """, (
                    data["descripcion"],
                ))

                conn.commit()
                cursor.close()
                conn.close()

                print("🎉 Condicion guardado correctamente.")
                return redirect('condicion_list')

            except Exception as e:
                print("❌ Error al guardar en BD:", str(e))
                form.add_error(None, f"Error al guardar: {e}")
        else:
            print("⚠️ Errores del formulario:", form.errors)

    else:
        print("📄 Mostrando formulario vacío (GET)")
        form = CondicionForm()

    return render(request, 'condicion fisica/condicion_form.html', {
        'form': form,
        'is_editing': False
    })

def condicion_delete(request, id_condicion_fisica):  # Cambié 'id' por 'id_cliente'
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtenemos el cliente por ID
    cursor.execute("SELECT descripcion FROM SGG_P_CondicionFisica WHERE id_condicion_fisica = ?", (id_condicion_fisica,))
    condicion = cursor.fetchone()

    if not condicion:
        conexion.close()
        return redirect('condicion_list')  # Cliente no existe, volvemos

    nombre_condicion = condicion[0]

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM SGG_P_CondicionFisica WHERE id_condicion_fisica = ?", (id_condicion_fisica,))
            conexion.commit()
            conexion.close()
            return redirect('condicion_list')
        except pyodbc.IntegrityError:
            conexion.close()
            return render(request, 'condicion fisica/delete.html', {
                'id_cliente': id_condicion_fisica,  # Cambié 'id' por 'id_cliente'
                'nombre': nombre_condicion,
                'error': 'No se puede eliminar el cliente porque tiene inscripciones asociadas.'
            })

    conexion.close()
    return render(request, 'condicion fisica/delete.html', {
        'id_cliente': id_condicion_fisica,  # Cambié 'id' por 'id_cliente'
        'nombre': nombre_condicion
    })

def condicion_update(request, id_cliente):
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
        query = "SELECT descripcion FROM SGG_P_CondicionFisica WHERE id_condicion_fisica = ?"
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
            form = CondicionForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(f"   - Datos del formulario válidos: {data}")
                
                cursor.execute("""
                    UPDATE SGG_P_CondicionFisica
                    SET descripcion = ?
                    WHERE id_condicion_fisica = ?
                """, (
                    data['descripcion'],
                    id_cliente
                ))
                conn.commit()
                print(f"   - ✅ Cliente actualizado exitosamente")
                cursor.close()
                conn.close()
                return redirect('condicion_list')
            else:
                print(f"   - ❌ Errores en el formulario: {form.errors}")
        else:
            print(f"   - Mostrando formulario GET")
            form = CondicionForm(initial=cliente_actual)

        cursor.close()
        conn.close()

        print(f"   - Renderizando template con is_editing=True")
        return render(request, 'condicion fisica/condicion_form.html', {
            'form': form,
            'is_editing': True,
            'id_condicion_fisica': id_cliente,
        })

    except Exception as e:
        print(f"   - ❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
        
        return render(request, 'condicion fisica/condicion_form.html', {
            'form': CondicionForm(),
            'error': f"Ocurrió un error: {e}",
            'is_editing': False,
        })