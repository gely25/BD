# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class SggMActividad(models.Model):
    id_actividad = models.AutoField(primary_key=True)
    id_tipo_actividad = models.ForeignKey('SggPTipoactividad', models.DO_NOTHING, db_column='id_tipo_actividad')
    nombre = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    descripcion = models.CharField(max_length=500, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    dia_semana = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    cupo_maximo = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SGG_M_Actividad'


class SggMCliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    dni = models.CharField(unique=True, max_length=20, db_collation='Modern_Spanish_CI_AS')
    telefono = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    email = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    genero = models.CharField(max_length=10, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SGG_M_Cliente'


class SggMEmpleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    id_rol = models.ForeignKey('SggPRol', models.DO_NOTHING, db_column='id_rol')
    nombre = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    dni = models.CharField(unique=True, max_length=20, db_collation='Modern_Spanish_CI_AS')
    telefono = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    email = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SGG_M_Empleado'


class SggMMembresia(models.Model):
    id_membresia = models.AutoField(primary_key=True)
    id_tipo_membresia = models.ForeignKey('SggPTipomembresia', models.DO_NOTHING, db_column='id_tipo_membresia')
    id_duracion = models.ForeignKey('SggPDuracion', models.DO_NOTHING, db_column='id_duracion')
    precio_actual = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.CharField(max_length=500, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SGG_M_Membresia'


class SggPCondicionfisica(models.Model):
    id_condicion_fisica = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'SGG_P_CondicionFisica'


class SggPDuracion(models.Model):
    id_duracion = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS')
    dias = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'SGG_P_Duracion'


class SggPRol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'SGG_P_Rol'


class SggPTipoactividad(models.Model):
    id_tipo_actividad = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'SGG_P_TipoActividad'


class SggPTipomembresia(models.Model):
    id_tipo_membresia = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')

    class Meta:
        managed = False
        db_table = 'SGG_P_TipoMembresia'


class SggTAsistencia(models.Model):
    id_asistencia = models.AutoField(primary_key=True)
    id_inscripcion = models.ForeignKey('SggTInscripcion', models.DO_NOTHING, db_column='id_inscripcion')
    id_actividad = models.ForeignKey(SggMActividad, models.DO_NOTHING, db_column='id_actividad')
    id_empleado = models.ForeignKey(SggMEmpleado, models.DO_NOTHING, db_column='id_empleado')
    fecha = models.DateField()

    class Meta:
        managed = False
        db_table = 'SGG_T_Asistencia'


class SggTEvaluacionfisica(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    id_inscripcion = models.ForeignKey('SggTInscripcion', models.DO_NOTHING, db_column='id_inscripcion')
    id_empleado = models.ForeignKey(SggMEmpleado, models.DO_NOTHING, db_column='id_empleado')
    peso = models.DecimalField(max_digits=5, decimal_places=2)
    altura = models.DecimalField(max_digits=5, decimal_places=2)
    fecha = models.DateField()
    grasa_corporal = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    presion_arterial = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    id_condicion_fisica = models.ForeignKey(SggPCondicionfisica, models.DO_NOTHING, db_column='id_condicion_fisica', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SGG_T_EvaluacionFisica'


class SggTInscripcion(models.Model):
    id_inscripcion = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(SggMCliente, models.DO_NOTHING, db_column='id_cliente')
    id_membresia = models.ForeignKey(SggMMembresia, models.DO_NOTHING, db_column='id_membresia')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    precio_pagado = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SGG_T_Inscripcion'


class SggTRutina(models.Model):
    id_rutina = models.AutoField(primary_key=True)
    id_evaluacion = models.ForeignKey(SggTEvaluacionfisica, models.DO_NOTHING, db_column='id_evaluacion')
    nombre_rutina = models.CharField(max_length=255, db_collation='Modern_Spanish_CI_AS')
    nivel = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS')
    descripcion = models.TextField(db_collation='Modern_Spanish_CI_AS', blank=True, null=True)
    objetivo = models.CharField(max_length=500, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SGG_T_Rutina'


class SggTSeguimientorutina(models.Model):
    id_seguimiento = models.AutoField(primary_key=True)
    id_rutina = models.ForeignKey(SggTRutina, models.DO_NOTHING, db_column='id_rutina')
    dia_semana = models.CharField(max_length=20, db_collation='Modern_Spanish_CI_AS')
    fecha_programada = models.DateField()
    estado_cumplimiento = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SGG_T_SeguimientoRutina'
