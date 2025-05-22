from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import UsuarioLoginForm

app_name = 'usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='usuarios/login.html',
        authentication_form=UsuarioLoginForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='usuarios:login'), name='logout'),
    path('cadastro/', views.cadastro_usuario, name='cadastro'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
]
