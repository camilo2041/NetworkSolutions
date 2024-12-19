from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .forms import CustomUserCreationForm, InformacionAdicionalUsuarioForm
from inventario.models import Producto, Categoria
from .models import Servicio, InformacionAdicionalUsuario
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    user = request.user if request.user.is_authenticated else None
    is_staff = user.is_staff if user else False
    
    categorias = Categoria.objects.all()  # Obtén todas las categorías
    servicios = Servicio.objects.all()  # Obtén todos los servicios
    
    # Validar si las consultas están vacías
    no_categorias = not categorias.exists()  # Devuelve True si no hay categorías
    no_servicios = not servicios.exists()  # Devuelve True si no hay servicios

    # Pasamos todos los datos en un único diccionario
    return render(request, 'index.html', {
        'user': user,
        'is_staff': is_staff,
        'categorias': categorias,
        'servicios': servicios,
        'no_categorias': no_categorias,
        'no_servicios': no_servicios,
    })


def registro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'login/registro.html', {'form': form})

@csrf_exempt 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bienvenido {}'.format(user.username))
            return redirect('index')
        else: 
            messages.error(request, 'Usuario o contraseña incorrectos')
    user = request.user if request.user.is_authenticated else None
    is_superadmin = False
    if user and user.is_superuser:
        is_superadmin = True
    return render(request, 'login/login.html', {'is_superadmin': is_superadmin})

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión finalizada')
    return redirect('index')

def productos_por_categoria(request, categoria_slug):
    # Obtener la categoría por su slug
    categoria_obj = get_object_or_404(Categoria, slug=categoria_slug)
    
    # Filtrar los productos por la categoría obtenida
    productos = Producto.objects.filter(categoria=categoria_obj)
    
    # Pasar los productos y la categoría al template
    return render(request, 'productos.html', {
        'categoria': categoria_obj,
        'productos': productos,
    })
    
def servicio_detalle(request, slug):
    servicio = get_object_or_404(Servicio, slug=slug)
    return render(request, 'servicio.html', {'servicio': servicio})


# Vista personalizada para cambiar la contraseña
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'login/cambiar_contraseña.html'
    success_message = "¡Contraseña cambiada exitosamente!"
    success_url = reverse_lazy('cambiar_contrasena')

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user)
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Hubo un error al cambiar la contraseña. Verifica los datos ingresados.")
        return super().form_invalid(form)
    
@login_required
def perfil_usuario(request):
    # Obtener la información adicional del usuario logueado
    try:
        # Se obtiene la información adicional asociada al usuario logueado
        informacion_adicional = InformacionAdicionalUsuario.objects.get(user=request.user)
    except InformacionAdicionalUsuario.DoesNotExist:
        # Si no existe, se crea una nueva entrada vacía para el usuario
        informacion_adicional = InformacionAdicionalUsuario(user=request.user)
        informacion_adicional.save()

    # Manejo del formulario para actualizar la información adicional
    if request.method == 'POST':
        form = InformacionAdicionalUsuarioForm(request.POST, instance=informacion_adicional)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Tu perfil se ha actualizado exitosamente!")
            return redirect('perfil_usuario')
        else:
            messages.error(request, "Hubo un error al actualizar tu perfil.")
    else:
        form = InformacionAdicionalUsuarioForm(instance=informacion_adicional)

    # Pasar al contexto la información del usuario logueado
    return render(request, 'perfil.html', {
        'form': form,
        'informacion_adicional': informacion_adicional,
        'user': request.user  # Este es el usuario logueado
    })