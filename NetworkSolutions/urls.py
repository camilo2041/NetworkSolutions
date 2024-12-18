"""
URL configuration for NetworkSolutions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from landing import views
from django.contrib.auth import views as auth_views
from facturacion.admin_views import descargar_factura_pdf

urlpatterns = [
    path('panel_administrador_network_solutions/', admin.site.urls, name='admin:index'),
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('categoria/<slug:categoria_slug>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('servicio/<slug:slug>/', views.servicio_detalle, name='servicio'),
    path('cambiar-contrasena/', views.CustomPasswordChangeView.as_view(), name='login/cambiar_contraseña'),
    path('factura/<int:factura_id>/descargar-pdf/', descargar_factura_pdf, name='descargar_factura_pdf'),
]

# Servir archivos multimedia en desarrollo (solo para DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)