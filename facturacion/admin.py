from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from .models import Factura, DetalleFactura
from inventario.models import Producto
from landing.models import InformacionAdicionalUsuario
from django.conf import settings

# Clase Inline para gestionar los detalles de la factura
class DetalleFacturaInline(admin.TabularInline):
    model = DetalleFactura
    extra = 1  # Número de filas vacías que aparecerán por defecto
    fields = ['producto', 'cantidad', 'precio_unitario', 'subtotal']
    readonly_fields = ['subtotal']  # No permitir que el subtotal sea editado directamente
    autocomplete_fields = ['producto']  # Autocompletar los productos desde el admin de inventario

    def subtotal(self, obj):
        return obj.subtotal()
    subtotal.short_description = "Subtotal"


# Clase para administrar Facturas
@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'fecha', 'total')
    list_filter = ('fecha',)  # Filtrar por fecha de creación
    search_fields = ('usuario__username',)  # Buscar por nombre de usuario
    inlines = [DetalleFacturaInline]
    actions = ['generar_pdf_factura']  # Agregar la acción personalizada para generar PDF

    def save_model(self, request, obj, form, change):
        """
        Sobreescribe el método save_model para calcular el total de la factura
        al momento de guardarla.
        """
        obj.save()  # Primero guarda la factura para asignarle un ID
        obj.calcular_total()  # Luego calcula el total después de guardarla
        super().save_model(request, obj, form, change)

    def generar_pdf_factura(self, request, queryset):
        """
        Genera un archivo PDF para una o más facturas seleccionadas desde el admin.
        """
        if queryset.count() > 1:
            return HttpResponse("Por favor selecciona solo una factura para descargar el PDF.", status=400)

        factura = queryset.first()

        # Recuperar los datos del usuario asociado a la factura
        usuario = factura.usuario  # El usuario relacionado con la factura
        usuario_full_name = usuario.get_full_name() if usuario.get_full_name() else "Nombre no disponible"
        usuario_email = usuario.email if usuario.email else "Correo no disponible"
        
        # Acceder a la información adicional del usuario
        try:
            info_adicional = InformacionAdicionalUsuario.objects.get(user=usuario)
            usuario_direccion = info_adicional.direccion_residencia if info_adicional.direccion_residencia else "Dirección no disponible"
            usuario_telefono = info_adicional.numero_telefonico if info_adicional.numero_telefonico else "Teléfono no disponible"
        except InformacionAdicionalUsuario.DoesNotExist:
            usuario_direccion = 'Dirección no disponible'
            usuario_telefono = 'Teléfono no disponible'

        # Configuración del PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Factura_{factura.id}.pdf"'

        # Crear el objeto canvas para generar el PDF
        p = canvas.Canvas(response, pagesize=letter)
        p.setFont("Helvetica", 12)

        # Añadir el logo (ajustar la posición Y)
        logo_path = settings.MEDIA_ROOT + '/image/logo.jpg'  # Ajusta la ruta al logo de la empresa
        p.drawImage(logo_path, 50, 730, width=100, height=50)  # Mover el logo más abajo

        # Información de la factura
        p.setFont("Helvetica-Bold", 16)
        p.setFillColor(colors.orange)  # Usar color naranja para el título
        p.drawString(200, 750, f"FACTURA DE COMPRA")
        
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.black)  # Establecer texto en negro
        
        p.drawString(50, 715, f"Factura #{factura.id}")
        p.drawString(50, 700, f"Cliente: {usuario_full_name}")
        p.drawString(50, 680, f"Teléfono: {usuario_telefono}")
        p.drawString(50, 660, f"Dirección: {usuario_direccion}")
        p.drawString(50, 640, f"Correo: {usuario_email}")
        p.drawString(50, 620, f"Fecha: {factura.fecha.strftime('%d/%m/%Y')}")

        # Crear tabla con estilo
        p.setFont("Helvetica-Bold", 10)
        p.setFillColor(colors.black)  # Texto negro para los encabezados
        p.setStrokeColor(colors.black)
        p.setLineWidth(1)
        
        # Dibujar el fondo naranja para la cabecera de la tabla
        p.setFillColor(colors.orange)
        p.rect(50, 580, 500, 20, fill=1)
        
        # Escribir los encabezados de la tabla en negro
        p.setFillColor(colors.black)
        p.drawString(60, 585, "CANTIDAD")
        p.drawString(160, 585, "DESCRIPCIÓN")
        p.drawString(350, 585, "VALOR")
        p.drawString(450, 585, "COSTO TOTAL")

        # Escribir los productos
        p.setFont("Helvetica", 10)
        y_position = 560
        for detalle in factura.detalles.all():
            producto = detalle.producto
            subtotal = detalle.subtotal()  # Calcula el subtotal de ese detalle
            p.drawString(60, y_position, str(detalle.cantidad))
            p.drawString(160, y_position, producto.nombre)
            p.drawString(350, y_position, f"${detalle.precio_unitario:.2f}")
            p.drawString(450, y_position, f"${subtotal:.2f}")
            y_position -= 20  # Baja la posición Y para el siguiente producto

        # Dibujar línea horizontal para separar la tabla de los totales
        p.setStrokeColor(colors.black)
        p.line(50, y_position, 550, y_position)

        # Total de la factura
        p.setFont("Helvetica-Bold", 12)
        p.setFillColor(colors.orange)  # Total en naranja
        p.drawString(50, y_position - 30, f"TOTAL: ${factura.total:.2f}")

        # Información de contacto en el pie de página
        p.setFont("Helvetica", 8)
        p.setFillColor(colors.grey)
        p.drawString(50, 50, "Bogotá, Colombia")
        p.drawString(50, 40, "Tel: 318 123 4567")
        p.drawString(50, 30, "Rafael Velasco")  
        p.drawString(50, 30, "NETWORK SOLUTIONS")

        # Finaliza la página y guarda el PDF
        p.showPage()
        p.save()

        return response

    generar_pdf_factura.short_description = "Descargar PDF de la Factura"


# Clase para administrar DetalleFactura en el admin
@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = ('factura', 'producto', 'cantidad', 'precio_unitario', 'subtotal')
    search_fields = ('producto__nombre',)  # Buscar por nombre del producto
    readonly_fields = ('subtotal',)  # No permitir modificar el subtotal directamente
    list_filter = ('factura__fecha', 'producto__categoria')  # Filtrar por fecha de factura y categoría del producto
