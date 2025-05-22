from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class Usuario(AbstractUser):
    """
    Modelo personalizado de usuário para o sistema Casa da Cultura.
    Estende o modelo padrão do Django para incluir níveis de permissão específicos.
    """
    TIPO_USUARIO_CHOICES = [
        ('consulta', 'Consulta apenas'),
        ('cadastro', 'Cadastro e consulta'),
        ('admin', 'Administrador (CRUD total)'),
    ]
    
    tipo_usuario = models.CharField(
        max_length=10,
        choices=TIPO_USUARIO_CHOICES,
        default='consulta',
        verbose_name=_('Tipo de Usuário')
    )
    
    # Relacionamentos personalizados para o modelo de usuário
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('grupos'),
        blank=True,
        help_text=_(
            'Os grupos aos quais este usuário pertence. Um usuário terá todas as permissões '
            'concedidas a cada um de seus grupos.'
        ),
        related_name="usuario_set",
        related_query_name="usuario",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissões do usuário'),
        blank=True,
        help_text=_('Permissões específicas para este usuário.'),
        related_name="usuario_set",
        related_query_name="usuario",
    )
    
    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')
        
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):
        # Garante que a senha seja criptografada ao salvar
        super().save(*args, **kwargs)
        
        # Atribui permissões com base no tipo de usuário
        self.user_permissions.clear()
        
        if self.tipo_usuario == 'consulta':
            # Permissões apenas para visualização
            pass
        elif self.tipo_usuario == 'cadastro':
            # Permissões para cadastro e visualização
            pass
        elif self.tipo_usuario == 'admin':
            # Permissões totais (CRUD)
            pass
