

from sqlite3 import IntegrityError
from django.shortcuts import render
from core.services.cliente_service import obtener_clientes

def cliente_list(request):
    clientes = obtener_clientes()
    return render(request, 'cliente/cliente_list.html', {'clientes': clientes})




from django.shortcuts import render, redirect
from core.conexion import obtener_conexion
import pyodbc

def cliente_delete(request, id_cliente):  # Cambié 'id' por 'id_cliente'
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtenemos el cliente por ID
    cursor.execute("SELECT nombre FROM SGG_M_Cliente WHERE id_cliente = ?", (id_cliente,))
    cliente = cursor.fetchone()

    if not cliente:
        conexion.close()
        return redirect('cliente_list')  # Cliente no existe, volvemos

    nombre_cliente = cliente[0]

    if request.method == 'POST':
        try:
            cursor.execute("DELETE FROM SGG_M_Cliente WHERE id_cliente = ?", (id_cliente,))
            conexion.commit()
            conexion.close()
            return redirect('cliente_list')
        except pyodbc.IntegrityError:
            conexion.close()
            return render(request, 'cliente/delete.html', {
                'id_cliente': id_cliente,  # Cambié 'id' por 'id_cliente'
                'nombre': nombre_cliente,
                'error': 'No se puede eliminar el cliente porque tiene inscripciones asociadas.'
            })

    conexion.close()
    return render(request, 'cliente/delete.html', {
        'id_cliente': id_cliente,  # Cambié 'id' por 'id_cliente'
        'nombre': nombre_cliente
    })











        
        
        
        
        
from django.shortcuts import render, redirect
from django.http import HttpResponse
from core.forms import ClienteForm
from core.conexion import obtener_conexion

def cliente_update(request, id_cliente):
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
        query = "SELECT nombre, dni, telefono, email, fecha_nacimiento, genero FROM SGG_M_Cliente WHERE id_cliente = ?"
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
        nombre, dni, telefono, email, fecha_nacimiento, genero = row
        print(f"   - ✅ Cliente encontrado: {nombre}")

        cliente_actual = {
            'nombre': nombre,
            'dni': dni,
            'telefono': telefono,
            'email': email,
            'fecha_nacimiento': fecha_nacimiento,
            'genero': genero,
        }
        
        print(f"   - Datos del cliente: {cliente_actual}")

        if request.method == 'POST':
            print(f"   - Procesando POST")
            form = ClienteForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                print(f"   - Datos del formulario válidos: {data}")
                
                cursor.execute("""
                    UPDATE SGG_M_Cliente
                    SET nombre = ?, dni = ?, telefono = ?, email = ?, fecha_nacimiento = ?, genero = ?
                    WHERE id_cliente = ?
                """, (
                    data['nombre'],
                    data['dni'],
                    data['telefono'],
                    data['email'],
                    data['fecha_nacimiento'],
                    data['genero'],
                    id_cliente
                ))
                conn.commit()
                print(f"   - ✅ Cliente actualizado exitosamente")
                cursor.close()
                conn.close()
                return redirect('cliente_list')
            else:
                print(f"   - ❌ Errores en el formulario: {form.errors}")
        else:
            print(f"   - Mostrando formulario GET")
            form = ClienteForm(initial=cliente_actual)

        cursor.close()
        conn.close()

        print(f"   - Renderizando template con is_editing=True")
        return render(request, 'cliente/cliente_form.html', {
            'form': form,
            'is_editing': True,
            'id_cliente': id_cliente,
        })

    except Exception as e:
        print(f"   - ❌ ERROR GENERAL: {e}")
        import traceback
        traceback.print_exc()
        
        return render(request, 'cliente/cliente_form.html', {
            'form': ClienteForm(),
            'error': f"Ocurrió un error: {e}",
            'is_editing': False,
        })
        
        


import pyodbc
from django.shortcuts import render, redirect
from core.forms import ClienteForm

def cliente_create(request):
    if request.method == 'POST':
        print("📩 Formulario recibido (POST)")
        print("Datos POST:", request.POST)

        form = ClienteForm(request.POST)
        print("¿Formulario válido?:", form.is_valid())

        if form.is_valid():
            data = form.cleaned_data
            print("✅ Datos limpios:", data)

            try:
                # Conexión a SQL Server
              
                conn = pyodbc.connect(
                    'DRIVER={ODBC Driver 17 for SQL Server};'
                    'SERVER=DESKTOP-8M2K84V\\SQLEXPRESS;'  # corregido
                    'DATABASE=SGG;'
                    'Trusted_Connection=yes;'
                )

                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO SGG_M_Cliente (nombre, dni, telefono, email, fecha_nacimiento, genero)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    data['nombre'],
                    data['dni'],
                    data['telefono'],
                    data['email'],
                    data['fecha_nacimiento'],
                    data['genero'],
                ))

                conn.commit()
                cursor.close()
                conn.close()

                print("🎉 Cliente guardado correctamente.")
                return redirect('cliente_list')

            except Exception as e:
                print("❌ Error al guardar en BD:", str(e))
                form.add_error(None, f"Error al guardar: {e}")
        else:
            print("⚠️ Errores del formulario:", form.errors)

    else:
        print("📄 Mostrando formulario vacío (GET)")
        form = ClienteForm()

    return render(request, 'cliente/cliente_form.html', {
        'form': form,
        'is_editing': False
    })
