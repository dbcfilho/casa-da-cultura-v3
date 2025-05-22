# Manual Técnico - Sistema Casa da Cultura

## Visão Geral da Arquitetura

O Sistema Casa da Cultura foi desenvolvido utilizando a seguinte stack tecnológica:

- **Backend**: Python 3.11+ com Django 4+
- **Banco de Dados**: MySQL 8+
- **Frontend**: Django Templates com Bootstrap 5
- **Containerização**: Docker e Docker Compose

A arquitetura do sistema segue o padrão MVC (Model-View-Controller) implementado pelo Django, onde:
- **Models**: Representam as entidades do banco de dados
- **Views**: Controlam a lógica de negócio e o fluxo de dados
- **Templates**: Renderizam a interface do usuário

## Estrutura do Projeto

```
casa_da_cultura/
├── casa_da_cultura/        # Configurações principais do projeto Django
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Configurações do Django
│   ├── urls.py             # URLs principais
│   └── wsgi.py
├── core/                   # Aplicação principal
│   ├── admin.py            # Configurações do admin
│   ├── forms.py            # Formulários
│   ├── models.py           # Modelos de dados
│   ├── urls.py             # URLs da aplicação
│   ├── views.py            # Views/controladores
│   ├── utils/              # Utilitários
│   │   ├── exportacao.py   # Funções para exportação de dados
│   │   └── whatsapp.py     # Funções para envio de mensagens
│   └── templates/          # Templates HTML
│       └── core/           # Templates específicos da aplicação
├── usuarios/               # Aplicação de autenticação e usuários
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── templates/
│       └── usuarios/
├── static/                 # Arquivos estáticos
│   ├── css/
│   │   └── style.css       # Estilos personalizados
│   ├── js/
│   │   └── scripts.js      # Scripts personalizados
│   └── img/                # Imagens
├── templates/              # Templates globais
│   └── base.html           # Template base
├── media/                  # Arquivos enviados pelos usuários
├── docs/                   # Documentação
├── docker/                 # Arquivos relacionados ao Docker
│   └── mysql/
│       ├── init/           # Scripts de inicialização do MySQL
│       └── backup/         # Diretório para backups
├── venv/                   # Ambiente virtual Python
├── .env.example            # Exemplo de variáveis de ambiente
├── .gitignore              # Arquivos ignorados pelo Git
├── docker-compose.yml      # Configuração do Docker Compose
├── Dockerfile              # Configuração do container Django
├── manage.py               # Script de gerenciamento do Django
└── requirements.txt        # Dependências Python
```

## Modelos de Dados

### Usuario (usuarios/models.py)
Modelo personalizado de usuário que estende o modelo padrão do Django para incluir níveis de permissão específicos.

```python
class Usuario(AbstractUser):
    TIPO_USUARIO_CHOICES = [
        ('consulta', 'Consulta apenas'),
        ('cadastro', 'Cadastro e consulta'),
        ('admin', 'Administrador (CRUD total)'),
    ]
    
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='consulta')
```

### Pessoa (core/models.py)
Modelo principal para cadastro de pessoas atendidas pela Casa da Cultura.

```python
class Pessoa(models.Model):
    nome_completo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14, unique=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField()
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100, default="São Paulo")
    estado = models.CharField(max_length=2, default="SP")
    cep = models.CharField(max_length=9, blank=True, null=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    
    # Campos booleanos para categorização
    pai_ou_mae = models.BooleanField(default=False)
    ajuda_hospital = models.BooleanField(default=False)
    ajuda_creche = models.BooleanField(default=False)
    recebeu_cesta_basica = models.BooleanField(default=False)
    participa_oficinas = models.BooleanField(default=False)
    interesse_novas_turmas = models.BooleanField(default=False)
    tem_filhos = models.BooleanField(default=False)
    ajuda_transporte = models.BooleanField(default=False)
    
    observacoes = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ultima_atualizacao = models.DateTimeField(auto_now=True)
```

### MensagemPadrao (core/models.py)
Modelo para armazenar mensagens padrão para envio em datas comemorativas.

```python
class MensagemPadrao(models.Model):
    TIPO_MENSAGEM_CHOICES = [
        ('aniversario', 'Aniversário'),
        ('dia_das_maes', 'Dia das Mães'),
        ('dia_dos_pais', 'Dia dos Pais'),
        ('natal', 'Natal'),
        ('ano_novo', 'Ano Novo'),
        ('outro', 'Outro'),
    ]
    
    tipo = models.CharField(max_length=20, choices=TIPO_MENSAGEM_CHOICES)
    titulo = models.CharField(max_length=100)
    conteudo = models.TextField()
    ativa = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
```

### DataComemorativa (core/models.py)
Modelo para armazenar datas comemorativas personalizadas.

```python
class DataComemorativa(models.Model):
    nome = models.CharField(max_length=100)
    data = models.DateField()
    mensagem = models.ForeignKey(MensagemPadrao, on_delete=models.SET_NULL, null=True, blank=True)
    enviar_automaticamente = models.BooleanField(default=False)
```

### RegistroEnvioMensagem (core/models.py)
Modelo para registrar o histórico de envio de mensagens.

```python
class RegistroEnvioMensagem(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    mensagem = models.ForeignKey(MensagemPadrao, on_delete=models.SET_NULL, null=True)
    data_envio = models.DateTimeField(auto_now_add=True)
    sucesso = models.BooleanField(default=False)
    observacao = models.TextField(blank=True, null=True)
```

## Sistema de Autenticação e Permissões

O sistema utiliza um modelo de usuário personalizado (`Usuario`) que estende o modelo padrão do Django (`AbstractUser`). Isso permite a implementação de três níveis de permissão:

1. **Consulta apenas**: Acesso somente para visualização de dados
2. **Cadastro e consulta**: Acesso para visualização e cadastro/edição de dados
3. **Administrador**: Acesso total ao sistema (CRUD completo)

A verificação de permissões é implementada através de um decorador personalizado:

```python
def permissao_requerida(tipo_permissao):
    def decorator(view_func):
        @login_required
        def wrapped_view(request, *args, **kwargs):
            # Verificar permissões com base no tipo de usuário
            if tipo_permissao == 'consulta':
                # Todos os usuários logados podem consultar
                pass
            elif tipo_permissao == 'cadastro':
                # Apenas usuários com permissão de cadastro ou admin
                if request.user.tipo_usuario == 'consulta':
                    messages.error(request, 'Você não tem permissão para esta operação.')
                    return redirect('core:home')
            elif tipo_permissao == 'admin':
                # Apenas administradores
                if request.user.tipo_usuario != 'admin':
                    messages.error(request, 'Você não tem permissão para esta operação.')
                    return redirect('core:home')
            
            return view_func(request, *args, **kwargs)
        return wrapped_view
    return decorator
```

## Exportação de Dados

O sistema permite a exportação de dados em formatos CSV e PDF através de utilitários implementados em `core/utils/exportacao.py`:

```python
def exportar_para_csv(queryset, campos, nomes_campos, nome_arquivo="exportacao.csv"):
    # Implementação da exportação para CSV
    
def exportar_para_pdf(queryset, campos, nomes_campos, titulo, nome_arquivo="exportacao.pdf", orientacao='retrato'):
    # Implementação da exportação para PDF
```

## Envio de Mensagens via WhatsApp

O envio de mensagens via WhatsApp é implementado utilizando a biblioteca `pywhatkit`, através de utilitários em `core/utils/whatsapp.py`:

```python
def enviar_mensagem_whatsapp(numero_telefone, mensagem, aguardar_segundos=15, fechar_apos_segundos=10):
    # Implementação do envio de mensagem via WhatsApp
    
def enviar_mensagem_em_lote(lista_destinatarios, mensagem_template, personalizar_func=None):
    # Implementação do envio em lote
```

## Frontend

O frontend utiliza Django Templates com Bootstrap 5 para criar uma interface responsiva e moderna. Os estilos personalizados são definidos em `static/css/style.css`, com cores principais em tons de azul e laranja:

```css
:root {
    --primary-color: #0d6efd;     /* Azul principal */
    --primary-dark: #0a58ca;      /* Azul escuro */
    --primary-light: #cfe2ff;     /* Azul claro */
    --secondary-color: #fd7e14;   /* Laranja principal */
    --secondary-dark: #ca6510;    /* Laranja escuro */
    --secondary-light: #ffe5d0;   /* Laranja claro */
}
```

## Configuração do Docker

O sistema é containerizado utilizando Docker e Docker Compose, com os seguintes serviços:

1. **web**: Container Django com a aplicação
2. **db**: Container MySQL para o banco de dados
3. **backup**: Container para realizar backups automáticos do banco de dados

A configuração completa está definida no arquivo `docker-compose.yml`.

## Variáveis de Ambiente

As variáveis de ambiente sensíveis são armazenadas em um arquivo `.env` (não versionado). Um exemplo de configuração está disponível em `.env.example`:

```
# Variáveis do Django
DEBUG=False
SECRET_KEY=sua_chave_secreta_aqui
ALLOWED_HOSTS=localhost,127.0.0.1

# Configurações do Banco de Dados
DB_NAME=casa_da_cultura
DB_USER=casa_user
DB_PASSWORD=senha_segura_aqui
DB_HOST=db
DB_PORT=3306
DB_ROOT_PASSWORD=senha_root_segura_aqui

# Configurações de Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_de_app_aqui
```

## Dependências

As dependências Python estão listadas no arquivo `requirements.txt`:

```
django==4.2.*
mysqlclient==2.2.*
python-dotenv==1.1.*
pillow==11.2.*
reportlab==4.4.*
django-crispy-forms==2.4.*
django-filter==25.1.*
pywhatkit==5.4.*
gunicorn==21.2.*
crispy-bootstrap5==2023.10.*
```

## Considerações de Segurança

1. **Senhas**: Todas as senhas são armazenadas de forma criptografada utilizando o sistema padrão do Django
2. **CSRF Protection**: Proteção contra ataques CSRF em todos os formulários
3. **Variáveis de Ambiente**: Dados sensíveis são armazenados em variáveis de ambiente
4. **Permissões**: Sistema de permissões por tipo de usuário
5. **Validação de Dados**: Validação de dados em formulários e modelos

## Manutenção e Backup

O sistema inclui um serviço de backup automático diário do banco de dados, configurado no Docker Compose:

```yaml
backup:
  image: mysql:8.0
  volumes:
    - ./docker/mysql/backup:/backup
  env_file:
    - ./.env
  depends_on:
    - db
  command: >
    sh -c "echo '0 0 * * * mysqldump -h db -u ${DB_USER} -p${DB_PASSWORD} ${DB_NAME} > /backup/backup_$$(date +\"%Y%m%d\").sql' > /var/spool/cron/crontabs/root && cron -f"
  restart: always
```

Os backups são armazenados no diretório `docker/mysql/backup/` e podem ser acessados pelo administrador do sistema.

## Extensibilidade

O sistema foi projetado para ser facilmente extensível:

1. **Novos Campos**: Adicionar novos campos ao modelo `Pessoa` é simples e não requer grandes alterações
2. **Novas Funcionalidades**: A estrutura modular permite adicionar novas funcionalidades sem afetar as existentes
3. **Personalização Visual**: Os estilos podem ser facilmente personalizados através do arquivo CSS

## Troubleshooting

### Problemas Comuns e Soluções

1. **Erro de Conexão com o Banco de Dados**:
   - Verificar se o serviço MySQL está em execução
   - Verificar as credenciais no arquivo `.env`
   - Verificar se o volume do MySQL está corretamente mapeado

2. **Erro no Envio de Mensagens via WhatsApp**:
   - Verificar se o WhatsApp Web está configurado no navegador
   - Verificar se o número de telefone está no formato correto
   - Aumentar o tempo de espera na função `enviar_mensagem_whatsapp`

3. **Problemas de Permissão**:
   - Verificar se o usuário tem o nível de permissão adequado
   - Verificar se o decorador `permissao_requerida` está sendo utilizado corretamente

4. **Erros de Exportação**:
   - Verificar se as bibliotecas `csv` e `reportlab` estão instaladas
   - Verificar se os campos a serem exportados existem no modelo

## Contato e Suporte

Para suporte técnico ou dúvidas sobre o sistema, entre em contato com a equipe de desenvolvimento.
