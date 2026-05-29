from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ConfigSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_clinica', models.CharField(default='Gaturno', max_length=100)),
                ('slogan', models.CharField(blank=True, default='Tu clínica veterinaria de confianza', max_length=250)),
                ('direccion', models.CharField(blank=True, max_length=300)),
                ('horario', models.CharField(blank=True, max_length=300)),
                ('telefono', models.CharField(blank=True, max_length=30)),
                ('whatsapp', models.CharField(blank=True, max_length=30, help_text='Solo dígitos con código de país, ej: 595981234567')),
                ('email_contacto', models.EmailField(blank=True)),
                ('instagram', models.URLField(blank=True)),
                ('facebook', models.URLField(blank=True)),
                ('google_maps_embed', models.TextField(blank=True)),
                ('texto_hero', models.CharField(blank=True, default='Cuidamos a tu mascota como si fuera nuestra', max_length=500)),
            ],
            options={
                'verbose_name': 'Configuración del Sitio Web',
                'verbose_name_plural': 'Configuración del Sitio Web',
            },
        ),
        migrations.CreateModel(
            name='GaleriaFoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=100)),
                ('foto', models.ImageField(upload_to='galeria/')),
                ('descripcion', models.CharField(blank=True, max_length=200)),
                ('orden', models.PositiveIntegerField(default=0)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Foto de Galería',
                'verbose_name_plural': 'Galería de Fotos',
                'ordering': ['orden', '-id'],
            },
        ),
        migrations.CreateModel(
            name='ProductoWeb',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('descripcion', models.TextField(blank=True)),
                ('precio', models.DecimalField(decimal_places=0, max_digits=12)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='productos_web/')),
                ('disponible', models.BooleanField(default=True)),
                ('orden', models.PositiveIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Producto del Petshop',
                'verbose_name_plural': 'Productos del Petshop',
                'ordering': ['orden', 'nombre'],
            },
        ),
    ]
