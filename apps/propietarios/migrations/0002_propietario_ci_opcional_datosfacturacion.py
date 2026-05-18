"""
Migración segura — no destruye datos existentes.
Cambios:
  1. numero_documento: NOT NULL unique → NULL unique (CI ahora opcional)
  2. HistoricalPropietario: mismo campo, solo agrega blank=True/null=True
  3. Nuevo modelo DatosFacturacion (tabla vacía, no afecta propietarios actuales)
"""
import django.db.models.deletion
import simple_history.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propietarios', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # 1. Propietario.numero_documento: permitir NULL
        migrations.AlterField(
            model_name='propietario',
            name='numero_documento',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
        # 2. Propietario.tipo_documento: permitir blank (coherente con CI opcional)
        migrations.AlterField(
            model_name='propietario',
            name='tipo_documento',
            field=models.CharField(
                blank=True,
                choices=[('ci', 'Cédula'), ('ruc', 'RUC'), ('pasaporte', 'Pasaporte')],
                default='ci',
                max_length=15,
            ),
        ),
        # 3. HistoricalPropietario.numero_documento: misma relajación
        migrations.AlterField(
            model_name='historicalpropietario',
            name='numero_documento',
            field=models.CharField(blank=True, db_index=True, max_length=20, null=True),
        ),
        # 4. HistoricalPropietario.tipo_documento
        migrations.AlterField(
            model_name='historicalpropietario',
            name='tipo_documento',
            field=models.CharField(
                blank=True,
                choices=[('ci', 'Cédula'), ('ruc', 'RUC'), ('pasaporte', 'Pasaporte')],
                default='ci',
                max_length=15,
            ),
        ),
        # 5. Nueva tabla DatosFacturacion
        migrations.CreateModel(
            name='DatosFacturacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razon_social', models.CharField(max_length=200, verbose_name='Razón Social / Nombre')),
                ('ruc', models.CharField(max_length=20, verbose_name='RUC')),
                ('propietario', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='datos_facturacion',
                    to='propietarios.propietario',
                )),
            ],
            options={
                'verbose_name': 'Datos de Facturación',
                'verbose_name_plural': 'Datos de Facturación',
            },
        ),
    ]
