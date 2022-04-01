from django import forms
from hbcommons.models import Usuario

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'nickname', 'email', 'photo']