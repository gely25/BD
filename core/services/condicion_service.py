from core.conexion import obtener_conexion


def obtener_condiciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_condicion_fisica, descripcion  
        FROM SGG_P_CondicionFisica
    """)

    columns = [column[0] for column in cursor.description]
    condiciones = [dict(zip(columns, row)) for row in cursor.fetchall()]
    conexion.close()
    return condiciones