from django.db import models
from django.utils.text import slugify

class Categoria(models.Model):
    Nombre_categoria = models.CharField(max_length=100)
    Explicacion_de_producto = models.TextField()
    imagen_categoria = models.ImageField(upload_to='image/categorias/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.Nombre_categoria


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.Nombre_categoria)
        super().save(*args, **kwargs)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT, related_name='productos')  # Relación con categoría
    descripcion = models.TextField() # Descripción detallada
    stock = models.IntegerField(default=0)  # Cantidad disponible
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del producto
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Descuento en porcentaje
    imagen = models.ImageField(upload_to='image/productos/', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación
    activo = models.BooleanField(default=True)  # Si el producto está activo

    def __str__(self):
        return f"{self.nombre} ({self.categoria.Nombre_categoria})"

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['-fecha_creacion']  # Ordenar por los más recientes

