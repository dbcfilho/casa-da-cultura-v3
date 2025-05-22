# README - Sistema Casa da Cultura

![Casa da Cultura](static/img/logo.png)

## Sobre o Projeto

O Sistema Casa da Cultura é uma aplicação web completa para gerenciamento de cadastros e atendimentos sociais, desenvolvida para facilitar o trabalho de projetos sociais no acompanhamento de pessoas atendidas, envio de mensagens em datas comemorativas e geração de relatórios estatísticos.

## Tecnologias Utilizadas

- **Backend**: Python 3.11+ com Django 4+
- **Banco de Dados**: MySQL 8+
- **Frontend**: Django Templates com Bootstrap 5
- **Containerização**: Docker e Docker Compose

## Funcionalidades Principais

- **Cadastro de Pessoas**: Gerenciamento completo de cadastros com informações pessoais e categorização
- **Aniversariantes**: Identificação e envio de mensagens para aniversariantes do dia e do mês
- **Datas Comemorativas**: Configuração de datas especiais para envio automático de mensagens
- **Envio de Mensagens**: Integração com WhatsApp para envio de mensagens personalizadas
- **Dashboard**: Visualização de estatísticas e gráficos para análise de dados
- **Exportação**: Geração de relatórios em formatos CSV e PDF
- **Controle de Acesso**: Três níveis de permissão (consulta, cadastro e administrador)

## Estrutura do Projeto

```
casa_da_cultura/
├── casa_da_cultura/        # Configurações principais do projeto Django
├── core/                   # Aplicação principal com funcionalidades do sistema
├── usuarios/               # Aplicação de autenticação e usuários
├── static/                 # Arquivos estáticos (CSS, JS, imagens)
├── templates/              # Templates globais
├── media/                  # Arquivos enviados pelos usuários
├── docs/                   # Documentação
├── docker/                 # Arquivos relacionados ao Docker
├── venv/                   # Ambiente virtual Python
├── docker-compose.yml      # Configuração do Docker Compose
├── Dockerfile              # Configuração do container Django
└── requirements.txt        # Dependências Python
```

## Documentação

A documentação completa do sistema está disponível na pasta `docs/`:

- [Diagrama ER](docs/diagrama_er.md): Estrutura do banco de dados
- [Diagramas UML](docs/diagramas_uml.md): Casos de uso e fluxo principal
- [Manual do Usuário](docs/manual_usuario.md): Guia para usuários finais
- [Manual Técnico](docs/manual_tecnico.md): Documentação técnica para desenvolvedores
- [Instruções de Instalação](docs/instrucoes_instalacao.md): Como instalar e executar o sistema

## Instalação Rápida

### Pré-requisitos

- Docker e Docker Compose instalados
- Git (opcional)

### Passos para Instalação

1. Clone o repositório ou baixe o código-fonte:
   ```bash
   git clone https://github.com/dbcfilho/casa-da-cultura.git
   cd casa-da-cultura
   ```

2. Crie o arquivo de variáveis de ambiente:
   ```bash
   cp .env.example .env
   ```

3. Edite o arquivo `.env` com suas configurações

4. Inicie os containers:
   ```bash
   docker-compose up --build
   ```

5. Acesse o sistema em http://localhost:8000

Para instruções detalhadas, consulte o [guia de instalação](docs/instrucoes_instalacao.md).

## Desenvolvimento

### Ambiente de Desenvolvimento Local

1. Crie um ambiente virtual Python:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure o banco de dados local no arquivo `.env`

4. Execute as migrações:
   ```bash
   python manage.py migrate
   ```

5. Crie um superusuário:
   ```bash
   python manage.py createsuperuser
   ```

6. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

Para suporte ou dúvidas sobre o sistema, entre em contato com a equipe de desenvolvimento.

---

Desenvolvido com ❤️ para a Casa da Cultura
