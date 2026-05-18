from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = [('admin','Administrador'),('veterinario','Veterinario'),
             ('asistente','Asistente'),('recepcionista','Recepcionista'),('esteticista','Esteticista')]
    rol = models.CharField(max_length=20, choices=ROLES, default='recepcionista')
    telefono = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='usuarios/', blank=True, null=True)
    matricula = models.CharField(max_length=30, blank=True)
    especialidad = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name='Usuario'; verbose_name_plural='Usuarios'

    def __str__(self):
        return f'{self.get_full_name() or self.username} ({self.get_rol_display()})'

    @property
    def nombre_completo(self):
        return self.get_full_name() or self.username

    @property
    def es_veterinario(self):
        return self.rol in ['veterinario', 'admin']

    @property
    def iniciales(self):
        fn = (self.first_name or '')[:1].upper()
        ln = (self.last_name or '')[:1].upper()
        return (fn + ln) or self.username[:2].upper()
