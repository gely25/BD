# limpiar_modelos.py
with open("core/models.py", "rb") as f:
    data = f.read()

# eliminar caracteres nulos
cleaned = data.replace(b"\x00", b"")

with open("core/models.py", "wb") as f:
    f.write(cleaned)

print("Archivo limpiado exitosamente.")
