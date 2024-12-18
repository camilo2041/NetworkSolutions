from django.contrib import admin
from django.utils.html import format_html
from .models import Producto, Categoria
from import_export.admin import ImportExportModelAdmin
from .resources import CategoriaResource, ProductoResource


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('Nombre_categoria', 'Explicacion_de_producto', 'imagen_thumbnail')
    list_display_links = ('Nombre_categoria',)  # El campo enlazable
    list_editable = ('Explicacion_de_producto',)
    search_fields = ('Nombre_categoria',)
    list_filter = ('Nombre_categoria',)
    list_per_page = 10

    def imagen_thumbnail(self, obj):
        if obj.imagen_categoria:
            return format_html('<img src="{}" width="50" />', obj.imagen_categoria.url)
        return "-"
    imagen_thumbnail.short_description = 'Imagen Categoría'

    fieldsets = (
        (None, {
            'fields': ('Nombre_categoria', 'Explicacion_de_producto', 'imagen_categoria',)
        }),
    )

@admin.register(Producto)
class ProductoAdmin(ImportExportModelAdmin):  # ImportExportModelAdmin
    list_display = ('nombre', 'categoria', 'descripcion', 'stock', 'precio', 'imagen_thumbnail')
    list_editable = ('descripcion', 'stock', 'precio')  # Solo campos específicos serán editables
    search_fields = ('nombre', 'categoria__Nombre_categoria', 'precio')
    list_filter = ('categoria', 'precio')
    list_per_page = 10
    list_display_links = ('nombre',)  # 'nombre' será el enlace a la vista de edición
    resource_class = ProductoResource  # Correcto: 'resource_class'
    
    def imagen_thumbnail(self, obj):
        if obj.imagen:
            return format_html('<img src="{}" width="50" />', obj.imagen.url)
        return "-"
    imagen_thumbnail.short_description = 'Imagen'

    fieldsets = (
        (None, {
            'fields': ('nombre', 'categoria', 'descripcion', 'stock', 'precio', 'imagen',)
        }),
    )
