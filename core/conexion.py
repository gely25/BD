import pyodbc

def obtener_conexion():
    """
    Conexión directa a tu base de datos SQL Server SGG usando autenticación confiable.
    """
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=SGG;"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)
