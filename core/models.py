from django.db import models
from django.utils import timezone

class Pessoa(models.Model):
    """
    Modelo para cadastro de pessoas atendidas pela Casa da Cultura.
    Inclui informações pessoais e campos booleanos para categorização.
    """
    # Informações pessoais
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    rg = models.CharField(max_length=20, blank=True, null=True, verbose_name="RG")
    data_nascimento = models.DateField(verbose_name="Data de Nascimento")
    
    # Informações de contato
    endereco = models.CharField(max_length=255, verbose_name="Endereço")
    bairro = models.CharField(max_length=100, verbose_name="Bairro")
    cidade = models.CharField(max_length=100, default="São Paulo", verbose_name="Cidade")
    estado = models.CharField(max_length=2, default="SP", verbose_name="Estado")
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name="CEP")
    telefone = models.CharField(max_length=15, verbose_name="Telefone")
    email = models.EmailField(blank=True, null=True, verbose_name="E-mail")
    
    # Campos booleanos para categorização
    pai_ou_mae = models.BooleanField(default=False, verbose_name="Pai ou Mãe")
    ajuda_hospital = models.BooleanField(default=False, verbose_name="Já foi ajudado com hospital?")
    ajuda_creche = models.BooleanField(default=False, verbose_name="Já foi ajudado com vaga em creche?")
    recebeu_cesta_basica = models.BooleanField(default=False, verbose_name="Já recebeu cestas básicas?")
    participa_oficinas = models.BooleanField(default=False, verbose_name="Participa de oficinas/aulas?")
    interesse_novas_turmas = models.BooleanField(default=False, verbose_name="Interesse em novas turmas?")
    tem_filhos = models.BooleanField(default=False, verbose_name="Tem filhos?")
    ajuda_transporte = models.BooleanField(default=False, verbose_name="Recebe ajuda de transporte?")
    
    # Campo de observações
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    # Campos de controle
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    ultima_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Última Atualização")
    
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"
        ordering = ['nome_completo']
    
    def __str__(self):
        return self.nome_completo
    
    def idade(self):
        """Calcula a idade da pessoa com base na data de nascimento."""
        hoje = timezone.now().date()
        idade = hoje.year - self.data_nascimento.year
        if (hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day):
            idade -= 1
        return idade
    
    def aniversario_hoje(self):
        """Verifica se a pessoa faz aniversário hoje."""
        hoje = timezone.now().date()
        return (hoje.month == self.data_nascimento.month and 
                hoje.day == self.data_nascimento.day)
    
    def aniversario_mes(self):
        """Verifica se a pessoa faz aniversário no mês atual."""
        hoje = timezone.now().date()
        return hoje.month == self.data_nascimento.month


class MensagemPadrao(models.Model):
    """
    Modelo para armazenar mensagens padrão para envio em datas comemorativas.
    """
    TIPO_MENSAGEM_CHOICES = [
        ('aniversario', 'Aniversário'),
        ('dia_das_maes', 'Dia das Mães'),
        ('dia_dos_pais', 'Dia dos Pais'),
        ('natal', 'Natal'),
        ('ano_novo', 'Ano Novo'),
        ('outro', 'Outro'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_MENSAGEM_CHOICES, verbose_name="Tipo de Mensagem")
    titulo = models.CharField(max_length=100, verbose_name="Título")
    conteudo = models.TextField(verbose_name="Conteúdo da Mensagem")
    ativa = models.BooleanField(default=True, verbose_name="Ativa")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    
    class Meta:
        verbose_name = "Mensagem Padrão"
        verbose_name_plural = "Mensagens Padrão"
        ordering = ['tipo', '-data_atualizacao']
    
    def __str__(self):
        return f"{self.get_tipo_display()}: {self.titulo}"


class DataComemorativa(models.Model):
    """
    Modelo para armazenar datas comemorativas personalizadas.
    """
    nome = models.CharField(max_length=100, verbose_name="Nome da Data")
    data = models.DateField(verbose_name="Data")
    mensagem = models.ForeignKey(MensagemPadrao, on_delete=models.SET_NULL, null=True, blank=True, 
                                verbose_name="Mensagem Padrão")
    enviar_automaticamente = models.BooleanField(default=False, verbose_name="Enviar Automaticamente")
    
    class Meta:
        verbose_name = "Data Comemorativa"
        verbose_name_plural = "Datas Comemorativas"
        ordering = ['data']
    
    def __str__(self):
        return f"{self.nome} ({self.data.strftime('%d/%m')})"


class RegistroEnvioMensagem(models.Model):
    """
    Modelo para registrar o histórico de envio de mensagens.
    """
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Pessoa")
    mensagem = models.ForeignKey(MensagemPadrao, on_delete=models.SET_NULL, null=True, verbose_name="Mensagem")
    data_envio = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")
    sucesso = models.BooleanField(default=False, verbose_name="Envio com Sucesso")
    observacao = models.TextField(blank=True, null=True, verbose_name="Observação")
    
    class Meta:
        verbose_name = "Registro de Envio"
        verbose_name_plural = "Registros de Envio"
        ordering = ['-data_envio']
    
    def __str__(self):
        return f"Mensagem para {self.pessoa} em {self.data_envio.strftime('%d/%m/%Y %H:%M')}"
