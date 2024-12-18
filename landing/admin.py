from django.contrib import admin
from .models import InformacionAdicionalUsuario, Servicio
from import_export.admin import ImportExportModelAdmin
from django.utils.html import format_html
from .resources import InformacionAdicionalUsuarioResource, ServicioResource

@admin.register(InformacionAdicionalUsuario)
class InformacionAdicionalUsuarioAdmin(ImportExportModelAdmin):
    list_display = ('user', 'numero_telefonico', 'direccion_residencia')
    list_filter = ('user',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'numero_telefonico', 'direccion_residencia')
    list_display_links = ('user',)
    resource_class = InformacionAdicionalUsuarioResource
    list_per_page = 10

@admin.register(Servicio)
class ServicioAdmin(ImportExportModelAdmin):
    list_display = ('servicio', 'tipo_servicio', 'especificaciones', 'imagen_thumbnail')
    list_filter = ('tipo_servicio',)
    search_fields = ('servicio', 'tipo_servicio', 'especificaciones')
    list_editable = ('tipo_servicio', 'especificaciones')
    list_display_links = ('servicio',)
    resource_class = ServicioResource
    list_per_page = 10

    def imagen_thumbnail(self, obj):
        if obj.imagen_servicio:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 5px;"/>', obj.imagen_servicio.url)
        return "-"
    imagen_thumbnail.short_description = 'Imagen'

    fieldsets = (
        (None, {
            'fields': ('servicio', 'tipo_servicio', 'especificaciones', 'imagen_servicio',)
        }),
    )
