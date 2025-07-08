from core.conexion import obtener_conexion

def obtener_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_cliente, nombre, dni, telefono, email, fecha_nacimiento, genero 
        FROM SGG_M_Cliente
    """)

    columns = [column[0] for column in cursor.description]
    clientes = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conexion.close()
    return clientes
