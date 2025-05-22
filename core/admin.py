from django.contrib import admin
from .models import Pessoa, MensagemPadrao, DataComemorativa, RegistroEnvioMensagem
from django.utils.html import format_html

admin.site.site_header = "Casa da Cultura Admin"
admin.site.site_title = "Administração Casa da Cultura"
admin.site.index_title = "Bem-vindo ao painel de administração"

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo Pessoa.
    """
    list_display = ('nome_completo', 'cpf', 'telefone', 'data_nascimento', 'idade', 'bairro', 'status_ajudas')
    list_filter = ('bairro', 'pai_ou_mae', 'ajuda_hospital', 'ajuda_creche', 'recebeu_cesta_basica', 
                  'participa_oficinas', 'tem_filhos', 'ajuda_transporte')
    search_fields = ('nome_completo', 'cpf', 'telefone', 'endereco', 'bairro', 'email')
    date_hierarchy = 'data_cadastro'
    readonly_fields = ('data_cadastro', 'ultima_atualizacao')
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome_completo', 'cpf', 'rg', 'data_nascimento')
        }),
        ('Contato', {
            'fields': ('endereco', 'bairro', 'cidade', 'estado', 'cep', 'telefone', 'email')
        }),
        ('Categorização', {
            'fields': ('pai_ou_mae', 'ajuda_hospital', 'ajuda_creche', 'recebeu_cesta_basica',
                      'participa_oficinas', 'interesse_novas_turmas', 'tem_filhos', 'ajuda_transporte')
        }),
        ('Observações', {
            'fields': ('observacoes',)
        }),
        ('Informações do Sistema', {
            'fields': ('data_cadastro', 'ultima_atualizacao'),
            'classes': ('collapse',)
        }),
    )
    
    def idade(self, obj):
        return f"{obj.idade()} anos"
    idade.short_description = "Idade"
    
    def status_ajudas(self, obj):
        ajudas = []
        if obj.ajuda_hospital:
            ajudas.append("Hospital")
        if obj.ajuda_creche:
            ajudas.append("Creche")
        if obj.recebeu_cesta_basica:
            ajudas.append("Cesta Básica")
        if obj.ajuda_transporte:
            ajudas.append("Transporte")
        
        if ajudas:
            return format_html("<span style='color: green;'>{}</span>", ", ".join(ajudas))
        return format_html("<span style='color: gray;'>Nenhuma</span>")
    status_ajudas.short_description = "Ajudas Recebidas"


@admin.register(MensagemPadrao)
class MensagemPadraoAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo MensagemPadrao.
    """
    list_display = ('titulo', 'tipo', 'ativa', 'data_atualizacao')
    list_filter = ('tipo', 'ativa')
    search_fields = ('titulo', 'conteudo')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        (None, {
            'fields': ('tipo', 'titulo', 'conteudo', 'ativa')
        }),
        ('Informações do Sistema', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )


@admin.register(DataComemorativa)
class DataComemorativaAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo DataComemorativa.
    """
    list_display = ('nome', 'data', 'mensagem', 'enviar_automaticamente')
    list_filter = ('enviar_automaticamente',)
    search_fields = ('nome',)
    date_hierarchy = 'data'
    raw_id_fields = ('mensagem',)


@admin.register(RegistroEnvioMensagem)
class RegistroEnvioMensagemAdmin(admin.ModelAdmin):
    """
    Configuração do admin para o modelo RegistroEnvioMensagem.
    """
    list_display = ('pessoa', 'mensagem', 'data_envio', 'sucesso')
    list_filter = ('sucesso', 'data_envio')
    search_fields = ('pessoa__nome_completo', 'observacao')
    date_hierarchy = 'data_envio'
    raw_id_fields = ('pessoa', 'mensagem')
    readonly_fields = ('data_envio',)
