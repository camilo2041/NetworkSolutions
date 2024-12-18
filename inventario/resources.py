from import_export import resources
from .models import Producto, Categoria

class CategoriaResource(resources.ModelResource):
    class Meta:
        model = Categoria
        fields = ('Nombre_categoria', 'Explicacion_de_producto', 'imagen_categoria')  # Usa el campo real de la imagen

class ProductoResource(resources.ModelResource):
    # Método para personalizar la exportación del campo 'categoria'
    def dehydrate_categoria(self, producto):
        # Retorna el nombre de la categoría en lugar del ID
        return producto.Categoria.Nombre_categoria if producto.Categoria else ""

    class Meta:
        model = Producto
        fields = ('nombre', 'categoria', 'descripcion', 'stock', 'precio', 'imagen')