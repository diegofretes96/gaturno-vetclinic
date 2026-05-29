from django.db import models


class ConfigSite(models.Model):
    """Singleton — solo una fila. Controla los datos del sitio público."""
    nombre_clinica = models.CharField(max_length=100, default='Gaturno')
    slogan = models.CharField(max_length=250, blank=True, default='Tu clínica veterinaria de confianza')
    direccion = models.CharField(max_length=300, blank=True)
    horario = models.CharField(max_length=300, blank=True, help_text='Ej: Lunes a Viernes 8:00 – 19:00')
    telefono = models.CharField(max_length=30, blank=True)
    whatsapp = models.CharField(
        max_length=30, blank=True,
        help_text='Solo dígitos con código de país, ej: 595981234567'
    )
    email_contacto = models.EmailField(blank=True)
    instagram = models.URLField(blank=True, help_text='URL completa del perfil de Instagram')
    facebook = models.URLField(blank=True, help_text='URL completa del perfil de Facebook')
    google_maps_embed = models.TextField(
        blank=True,
        help_text='Pegá la URL del iframe de Google Maps (solo el src="...")'
    )
    texto_hero = models.CharField(
        max_length=500, blank=True,
        default='Cuidamos a tu mascota como si fuera nuestra'
    )

    class Meta:
        verbose_name = 'Configuración del Sitio Web'
        verbose_name_plural = 'Configuración del Sitio Web'

    def __str__(self):
        return 'Configuración del sitio'

    def save(self, *args, **kwargs):
        self.pk = 1  # Singleton: siempre la misma fila
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            'nombre_clinica': 'Gaturno',
            'slogan': 'Tu clínica veterinaria de confianza',
        })
        return obj


class GaleriaFoto(models.Model):
    titulo = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='galeria/')
    descripcion = models.CharField(max_length=200, blank=True)
    orden = models.PositiveIntegerField(default=0, help_text='Menor número = aparece primero')
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['orden', '-id']
        verbose_name = 'Foto de Galería'
        verbose_name_plural = 'Galería de Fotos'

    def __str__(self):
        return self.titulo or f'Foto #{self.pk}'


class ProductoWeb(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=0)
    foto = models.ImageField(upload_to='productos_web/', blank=True, null=True)
    disponible = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0, help_text='Menor número = aparece primero')

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Producto del Petshop'
        verbose_name_plural = 'Productos del Petshop'

    def __str__(self):
        return self.nombre
