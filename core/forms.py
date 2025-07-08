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

        cursor.execute("SELECT id_tipo_membresia, nombre FROM SGG_P_TipoMembresia")
        self.fields['id_tipo_membresia'].choices = [(row[0], row[1]) for row in cursor.fetchall()]

        cursor.execute("SELECT id_duracion, descripcion FROM SGG_P_Duracion")
        self.fields['id_duracion'].choices = [(row[0], row[1]) for row in cursor.fetchall()]
        
        conn.close()





