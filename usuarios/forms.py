from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Usuario

class UsuarioCreationForm(UserCreationForm):
    """
    Formulário para criação de novos usuários com campos personalizados.
    """
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalização dos campos
        self.fields['username'].help_text = 'Nome de usuário para acesso ao sistema.'
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['tipo_usuario'].help_text = 'Define o nível de acesso do usuário no sistema.'

class UsuarioLoginForm(AuthenticationForm):
    """
    Formulário personalizado para login de usuários.
    """
    username = forms.CharField(label='Nome de usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    
    class Meta:
        model = Usuario
        fields = ('username', 'password')
