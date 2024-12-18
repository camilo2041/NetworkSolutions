from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import Factura

def descargar_factura_pdf(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_{factura.id}.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)

    # Encabezado
    p.drawString(100, 800, f"Factura #{factura.id}")
    p.drawString(100, 780, f"Usuario: {factura.usuario.username}")
    p.drawString(100, 760, f"Fecha: {factura.fecha.strftime('%d/%m/%Y')}")

    # Detalles
    y = 720
    for detalle in factura.detalles.all():
        p.drawString(100, y, f"{detalle.cantidad} x {detalle.producto.nombre} (Subtotal: ${detalle.subtotal()})")
        y -= 20

    # Total
    p.drawString(100, y - 20, f"Total: ${factura.total}")
    p.showPage()
    p.save()

    return response
