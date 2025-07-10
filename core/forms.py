from django import forms

GENERO_CHOICES = [
    ('Femenino', 'Femenino'),
    ('Masculino', 'Masculino'),
]

class ClienteForm(forms.Form):  # o forms.ModelForm si usas modelo
    nombre = forms.CharField(max_length=255)
    dni = forms.CharField(max_length=20)
    telefono = forms.CharField(max_length=20, required=False)
    email = forms.EmailField(required=False)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    genero = forms.ChoiceField(choices=GENERO_CHOICES)








from django import forms


estado = forms.ChoiceField(
    choices=[
        ('VIGENTE', 'VIGENTE'),
        ('VENCIDA', 'VENCIDA'),
        ('CANCELADA', 'CANCELADA'),
    ],
    label='Estado'
)


class InscripcionForm(forms.Form):
    id_cliente = forms.ChoiceField(label='Cliente')
    fecha_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de inicio'
    )
    fecha_fin = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Fecha de fin'
    )
    precio_pagado = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Precio pagado',
        required=True,
        min_value=0
    )
    estado = forms.ChoiceField(
        choices=[
            ('VIGENTE', 'VIGENTE'),
            ('VENCIDA', 'VENCIDA'),
            ('CANCELADA', 'CANCELADA'),
        ],
        label='Estado'
    )









from django import forms
from core.conexion import obtener_conexion

class MembresiaForm(forms.Form):
    id_tipo_membresia = forms.ChoiceField(label='Tipo de membresía')
    id_duracion = forms.ChoiceField(label='Duración')
    precio_actual = forms.DecimalField(label='Precio actual', max_digits=10, decimal_places=2)
    descripcion = forms.CharField(label='Descripción', required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        conn = obtener_conexion()
        cursor = conn.cursor()

        cursor.execute("SELECT id_tipo_membresia, descripcion FROM SGG_P_TipoMembresia")
        self.fields['id_tipo_membresia'].choices = [(str(row[0]), row[1]) for row in cursor.fetchall()]

        cursor.execute("SELECT id_duracion, descripcion FROM SGG_P_Duracion")
        self.fields['id_duracion'].choices = [(str(row[0]), row[1]) for row in cursor.fetchall()]

        conn.close()

    def clean_id_tipo_membresia(self):
        return int(self.cleaned_data['id_tipo_membresia'])

    def clean_id_duracion(self):
        return int(self.cleaned_data['id_duracion'])

    def clean_precio_actual(self):
        return float(self.cleaned_data['precio_actual'])

    def clean_descripcion(self):
        desc = self.cleaned_data['descripcion']
        return desc if desc.strip() else None









# core/forms.py
from django import forms

class TipoMembresiaForm(forms.Form):
    descripcion = forms.CharField(
        label='Descripción',
        max_length=255,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )













from django import forms
from core.conexion import obtener_conexion

class RutinaForm(forms.Form):
    id_evaluacion = forms.IntegerField()
    nombre_rutina = forms.CharField(max_length=255)
    nivel = forms.ChoiceField(label='Nivel')
    descripcion = forms.CharField(widget=forms.Textarea, required=False)
    objetivo = forms.CharField(max_length=500, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Cargar niveles de rutina desde la base de datos
        cursor.execute("SELECT DISTINCT nivel FROM SGG_T_Rutina")
        niveles = cursor.fetchall()
        self.fields['nivel'].choices = [(nivel[0], nivel[0]) for nivel in niveles]

        conn.close()


from django import forms
from core.conexion import obtener_conexion

class SeguimientoRutinaForm(forms.Form):
    ESTADO_CUMPLIMIENTO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CUMPLIDO', 'Cumplido'),
        ('FALTO', 'Faltó'),
    ]

    id_rutina = forms.ChoiceField(label="Rutina")
    fecha_programada = forms.DateField(
        label="Fecha Programada",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    estado_cumplimiento = forms.ChoiceField(
        label="Estado de Cumplimiento",
        choices=ESTADO_CUMPLIMIENTO_CHOICES
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        conn = obtener_conexion()
        cursor = conn.cursor()

        # Cargar rutinas desde la base de datos
        cursor.execute("SELECT id_rutina, nombre_rutina FROM SGG_T_Rutina")
        self.fields['id_rutina'].choices = [(row[0], row[1]) for row in cursor.fetchall()]

        conn.close()

        
        
        

        
class CondicionForm(forms.Form):
    descripcion = forms.CharField(max_length=255)

class RolForm(forms.Form):
    descripcion = forms.CharField(max_length=255)

class EmpleadoForm(forms.Form):
    id_rol = forms.ChoiceField(label='Rol')
    nombre = forms.CharField(max_length=255)
    dni = forms.CharField(max_length=20)
    telefono= forms.CharField(max_length=10)
    email = forms.EmailField()

class EvaluacionForm(forms.Form):
    id_inscripcion = forms.ChoiceField(label="Inscripcion")
    id_empleado = forms.ChoiceField(label="Empleado")
    peso = forms.DecimalField()
    altura = forms.DecimalField()
    fecha = forms.DateField(label='Fecha')
    grasa_corporal =forms.DecimalField()
    presion_arterial =forms.CharField(max_length=10)
    id_condicion_fisica= forms.ChoiceField(label="Condicion Fisica")