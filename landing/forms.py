from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import InformacionAdicionalUsuario


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Introduce un correo válido.")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        # Sobrescribe el método save para guardar campos adicionales
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añade clases personalizadas a los widgets de formulario
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-1 border-2 border-gray-300 rounded-md bg-gray-50 text-gray-800 focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-500'
            })
        
        # Personaliza los textos de ayuda
        self.fields['password1'].help_text = (
            "La contraseña debe cumplir con lo siguiente:<br>"
            "- No puede ser muy similar a su información personal.<br>"
            "- Debe contener al menos 8 caracteres.<br>"
            "- No puede ser una contraseña de uso común.<br>"
            "- No puede ser completamente numérica."
        )
        self.fields['password2'].help_text = "Introduce la misma contraseña para validarla."
        
class InformacionAdicionalUsuarioForm(forms.ModelForm):
    class Meta:
        model = InformacionAdicionalUsuario
        fields = ['numero_telefonico', 'direccion_residencia']