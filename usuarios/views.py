from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UsuarioCreationForm
from .models import Usuario

def cadastro_usuario(request):
    """
    View para cadastro de novos usuários.
    Apenas administradores podem cadastrar novos usuários.
    """
    # Verificar se o usuário é administrador
    if request.user.is_authenticated and request.user.tipo_usuario != 'admin':
        messages.error(request, 'Você não tem permissão para cadastrar novos usuários.')
        return redirect('core:home')
        
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('usuarios:login')
    else:
        form = UsuarioCreationForm()
    
    return render(request, 'usuarios/cadastro.html', {'form': form})

@login_required
def perfil_usuario(request):
    """
    View para exibição e edição do perfil do usuário logado.
    """
    if request.method == 'POST':
        # Lógica para atualização do perfil
        usuario = request.user
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.email = request.POST.get('email')
        usuario.save()
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('usuarios:perfil')
        
    return render(request, 'usuarios/perfil.html')

@login_required
def alterar_senha(request):
    """
    View para alteração de senha do usuário logado.
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Mantém o usuário logado após a alteração da senha
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada com sucesso!')
            return redirect('usuarios:perfil')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'usuarios/alterar_senha.html', {'form': form})
