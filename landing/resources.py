from import_export import resources 
from .models import InformacionAdicionalUsuario, Servicio

class InformacionAdicionalUsuarioResource(resources.ModelResource):
    class Meta:
        model = InformacionAdicionalUsuario
        fields = ('Fecha_nacimiento', 'Correo', 'Numero_telefonico', 'Dirreccion_recidencia')

class ServicioResource(resources.ModelResource):
    class Meta:
        model = Servicio
        fields = ('Servicio', 'Tipo_servicio', 'Especificaciones', 'imagen_servicio')   
