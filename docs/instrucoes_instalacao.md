# Instruções de Instalação - Sistema Casa da Cultura

Este documento contém instruções detalhadas para instalação e execução do Sistema Casa da Cultura em ambientes Ubuntu 24.04 e Windows, utilizando Docker.

## Pré-requisitos

### Para Ubuntu 24.04

1. **Docker e Docker Compose**:
   ```bash
   # Atualizar os repositórios
   sudo apt update
   
   # Instalar dependências necessárias
   sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
   
   # Adicionar chave GPG oficial do Docker
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   
   # Adicionar repositório do Docker
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   
   # Atualizar os repositórios novamente
   sudo apt update
   
   # Instalar Docker e Docker Compose
   sudo apt install -y docker-ce docker-compose
   
   # Adicionar seu usuário ao grupo docker para evitar usar sudo
   sudo usermod -aG docker $USER
   
   # Aplicar as mudanças de grupo (ou reinicie o sistema)
   newgrp docker
   ```

2. **Git** (opcional, para clonar o repositório):
   ```bash
   sudo apt install -y git
   ```

### Para Windows

1. **Docker Desktop**:
   - Baixe e instale o Docker Desktop para Windows no [site oficial](https://www.docker.com/products/docker-desktop)
   - Durante a instalação, siga as instruções para habilitar o WSL 2 (Windows Subsystem for Linux)
   - Após a instalação, inicie o Docker Desktop e verifique se está funcionando corretamente

2. **Git** (opcional, para clonar o repositório):
   - Baixe e instale o Git para Windows no [site oficial](https://git-scm.com/download/win)

## Instalação do Sistema

### Opção 1: Usando Git (recomendado)

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/casa-da-cultura.git
   cd casa-da-cultura
   ```

### Opção 2: Download Manual

1. **Baixe o código-fonte**:
   - Baixe o arquivo ZIP do projeto
   - Extraia o conteúdo para uma pasta de sua preferência
   - Abra um terminal/prompt de comando e navegue até a pasta extraída

### Configuração do Ambiente

1. **Crie o arquivo de variáveis de ambiente**:
   ```bash
   # No Linux/macOS
   cp .env.example .env
   
   # No Windows (PowerShell)
   Copy-Item .env.example .env
   ```

2. **Edite o arquivo .env com suas configurações**:
   - Abra o arquivo `.env` em um editor de texto
   - Modifique as variáveis conforme necessário, especialmente:
     - `SECRET_KEY`: Gere uma chave secreta forte
     - `DB_PASSWORD` e `DB_ROOT_PASSWORD`: Defina senhas seguras
     - Configurações de email se for utilizar envio de emails

## Execução do Sistema

### Iniciar os Containers

```bash
# Na pasta raiz do projeto
docker-compose up --build
```

Este comando irá:
1. Construir as imagens Docker necessárias
2. Criar os containers
3. Iniciar os serviços (Django, MySQL, backup)
4. Configurar volumes persistentes para dados e backups

Na primeira execução, o sistema irá:
1. Criar o banco de dados
2. Aplicar as migrações
3. Coletar arquivos estáticos

### Acessar o Sistema

Após iniciar os containers, o sistema estará disponível em:

- **URL**: http://localhost:8000
- **Painel Admin**: http://localhost:8000/admin

### Criar Superusuário (Administrador)

Para criar um usuário administrador, execute:

```bash
# Em um novo terminal/prompt de comando, com os containers em execução
docker-compose exec web python manage.py createsuperuser
```

Siga as instruções para criar o superusuário:
- Username
- Email
- Senha (não será exibida ao digitar)
- Confirmação de senha

## Parar o Sistema

Para parar os containers:

```bash
# Pressione Ctrl+C no terminal onde o docker-compose está em execução
# Ou, em outro terminal:
docker-compose down
```

Para parar e remover volumes (cuidado, isso apagará os dados):

```bash
docker-compose down -v
```

## Backup e Restauração

### Backup Manual

Para criar um backup manual do banco de dados:

```bash
docker-compose exec db mysqldump -u root -p casa_da_cultura > backup_manual.sql
# Digite a senha do root quando solicitado
```

### Restauração de Backup

Para restaurar um backup:

```bash
# Com os containers em execução
cat backup_arquivo.sql | docker-compose exec -T db mysql -u root -p casa_da_cultura
# Digite a senha do root quando solicitado
```

## Solução de Problemas

### Problemas de Permissão (Linux)

Se encontrar problemas de permissão nos volumes:

```bash
sudo chown -R $USER:$USER docker/
```

### Porta 8000 já em uso

Se a porta 8000 já estiver em uso, edite o arquivo `docker-compose.yml` e altere a porta mapeada:

```yaml
services:
  web:
    ports:
      - "8001:8000"  # Altere 8000 para outra porta disponível
```

### Problemas de Conexão com o Banco de Dados

Verifique se as variáveis de ambiente no arquivo `.env` estão corretas:

```
DB_NAME=casa_da_cultura
DB_USER=casa_user
DB_PASSWORD=sua_senha_aqui
DB_HOST=db
DB_PORT=3306
```

## Atualização do Sistema

Para atualizar o sistema após alterações no código:

```bash
# Pare os containers
docker-compose down

# Reconstrua as imagens
docker-compose up --build
```

## Considerações de Segurança

1. **Senhas**: Use senhas fortes para o banco de dados e superusuário
2. **Variáveis de Ambiente**: Não compartilhe o arquivo `.env` com informações sensíveis
3. **Backups**: Faça backups regulares e armazene-os em local seguro
4. **Produção**: Em ambiente de produção, configure HTTPS usando um proxy reverso como Nginx

## Próximos Passos

Após a instalação, recomendamos:

1. Criar usuários adicionais com diferentes níveis de permissão
2. Configurar mensagens padrão para datas comemorativas
3. Realizar um teste completo do sistema
4. Configurar backups externos para maior segurança

Para mais informações, consulte o Manual do Usuário e o Manual Técnico na pasta `docs/`.
