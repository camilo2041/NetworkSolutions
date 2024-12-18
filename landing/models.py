from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class InformacionAdicionalUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='informacion_adicional')
    numero_telefonico = models.CharField(max_length=15, verbose_name="Número Telefónico")
    direccion_residencia = models.CharField(max_length=255, verbose_name="Dirección de Residencia")

    class Meta:
        verbose_name = 'Información Adicional de Usuario'
        verbose_name_plural = 'Información Adicional de Usuarios'
        ordering = ['user__last_name', 'user__first_name']  # Ordenar alfabéticamente por nombre completo

    def __str__(self):
        return f"{self.numero_telefonico} - {self.user.username}"

class Servicio(models.Model):
    servicio = models.CharField(max_length=255, verbose_name="Nombre del Servicio")
    slug = models.SlugField(unique=True, blank=True, null=True)
    tipo_servicio = models.TextField(verbose_name="Tipo de Servicio")
    especificaciones = models.TextField(verbose_name="Especificaciones")
    imagen_servicio = models.ImageField(upload_to='image/servicios/', blank=True, null=True, verbose_name="Imagen del Servicio")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.servicio)  # Usar `servicio` para generar el slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.servicio