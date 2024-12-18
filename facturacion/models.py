from django.db import models
from django.conf import settings  # Para usar el modelo de Usuario
from inventario.models import Producto  # Importar el modelo de Producto

class Factura(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="facturas")
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calcular_total(self):
        """
        Calcula el total sumando los subtotales de los detalles.
        """
        total = sum(item.subtotal() for item in self.detalles.all())
        self.total = total
        self.save()

    def __str__(self):
        return f"Factura #{self.id} - {self.usuario.username}"


class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def subtotal(self):
        """
        Calcula el subtotal como precio_unitario * cantidad.
        Si precio_unitario es None, usa el precio con descuento del producto.
        """
        precio = self.precio_unitario or self.producto.precio_con_descuento()
        return precio * self.cantidad

    def save(self, *args, **kwargs):
        """
        Sobrescribe save para calcular el precio_unitario automáticamente.
        """
        if self.precio_unitario is None:  # Solo asigna si no está definido
            self.precio_unitario = self.producto.precio_con_descuento()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre}"
