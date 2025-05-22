# Diagramas UML - Casa da Cultura

## Diagrama de Casos de Uso

### Atores
1. **Usuário Consulta**: Acesso apenas para visualização de dados
2. **Usuário Cadastro**: Acesso para visualização e cadastro de dados
3. **Usuário Administrador**: Acesso total ao sistema (CRUD completo)

### Casos de Uso

#### Autenticação e Permissões
- **Fazer Login**: Todos os atores
- **Fazer Logout**: Todos os atores
- **Alterar Senha**: Todos os atores
- **Visualizar Perfil**: Todos os atores
- **Cadastrar Usuários**: Apenas Administrador
- **Gerenciar Permissões**: Apenas Administrador

#### Gestão de Pessoas
- **Visualizar Lista de Pessoas**: Todos os atores
- **Filtrar Pessoas**: Todos os atores
- **Visualizar Detalhes de Pessoa**: Todos os atores
- **Cadastrar Nova Pessoa**: Usuário Cadastro e Administrador
- **Editar Pessoa**: Usuário Cadastro e Administrador
- **Excluir Pessoa**: Apenas Administrador
- **Exportar Lista de Pessoas (CSV/PDF)**: Todos os atores

#### Aniversariantes e Mensagens
- **Visualizar Aniversariantes do Dia**: Todos os atores
- **Visualizar Aniversariantes do Mês**: Todos os atores
- **Enviar Mensagem de Aniversário**: Usuário Cadastro e Administrador
- **Gerenciar Mensagens Padrão**: Usuário Cadastro e Administrador
- **Gerenciar Datas Comemorativas**: Usuário Cadastro e Administrador

#### Dashboard e Estatísticas
- **Visualizar Dashboard**: Todos os atores
- **Visualizar Estatísticas de Ajudas**: Todos os atores
- **Visualizar Distribuição por Bairro**: Todos os atores
- **Visualizar Aniversariantes por Mês**: Todos os atores
- **Visualizar Cadastros por Período**: Todos os atores

## Diagrama de Fluxo Principal

### Fluxo de Cadastro e Gestão de Pessoas

1. **Início**: Usuário faz login no sistema
2. **Acesso ao Módulo de Pessoas**: Usuário acessa a lista de pessoas cadastradas
3. **Decisão**: Usuário decide entre visualizar, cadastrar, editar ou exportar
   - **Visualizar**: 
     - Usuário aplica filtros (opcional)
     - Sistema exibe lista de pessoas
     - Usuário seleciona pessoa para ver detalhes
     - Sistema exibe detalhes da pessoa
   - **Cadastrar** (se tiver permissão):
     - Usuário acessa formulário de cadastro
     - Usuário preenche dados pessoais e categorização
     - Sistema valida dados
     - Sistema salva novo cadastro
   - **Editar** (se tiver permissão):
     - Usuário seleciona pessoa para editar
     - Sistema exibe formulário preenchido
     - Usuário altera dados necessários
     - Sistema valida dados
     - Sistema salva alterações
   - **Exportar**:
     - Usuário aplica filtros (opcional)
     - Usuário seleciona formato (CSV ou PDF)
     - Sistema gera arquivo de exportação
     - Usuário faz download do arquivo
4. **Fim**: Usuário conclui operação

### Fluxo de Aniversariantes e Envio de Mensagens

1. **Início**: Usuário faz login no sistema
2. **Acesso ao Módulo de Aniversariantes**: Usuário acessa a página de aniversariantes
3. **Visualização**: Sistema exibe aniversariantes do dia e do mês
4. **Decisão**: Usuário decide se envia mensagem (se tiver permissão)
   - **Enviar Mensagem**:
     - Usuário seleciona pessoa para enviar mensagem
     - Sistema exibe formulário de envio
     - Usuário seleciona mensagem padrão
     - Usuário personaliza mensagem (opcional)
     - Usuário confirma envio
     - Sistema processa envio via WhatsApp
     - Sistema registra envio no histórico
5. **Fim**: Usuário conclui operação

### Fluxo de Dashboard e Estatísticas

1. **Início**: Usuário faz login no sistema
2. **Acesso ao Dashboard**: Usuário acessa a página de dashboard
3. **Visualização**: Sistema exibe estatísticas e gráficos
   - Total de pessoas cadastradas
   - Distribuição de ajudas por tipo
   - Distribuição por bairro
   - Aniversariantes por mês
   - Cadastros por período
4. **Fim**: Usuário visualiza estatísticas
