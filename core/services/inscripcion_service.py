from core.conexion import obtener_conexion
from core.conexion import obtener_conexion

def obtener_inscripciones():
    conn = obtener_conexion()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT 
        I.id_inscripcion,
        C.nombre AS nombre_cliente,
        TM.descripcion AS nombre_membresia,
        I.fecha_inicio,
        I.fecha_fin
    FROM SGG_T_Inscripcion I
    JOIN SGG_M_Cliente C ON I.id_cliente = C.id_cliente
    JOIN SGG_M_Membresia M ON I.id_membresia = M.id_membresia
    JOIN SGG_P_TipoMembresia TM ON M.id_tipo_membresia = TM.id_tipo_membresia
    """)

    columnas = [col[0] for col in cursor.description]
    resultados = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]

    conn.close()
    return resultados
