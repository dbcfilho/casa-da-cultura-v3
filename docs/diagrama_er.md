# Diagrama Entidade-Relacionamento (ER) - Casa da Cultura

## Entidades Principais

### Usuario
- id (PK)
- username
- password (criptografada)
- email
- first_name
- last_name
- tipo_usuario (consulta, cadastro, admin)
- is_active
- date_joined
- last_login

### Pessoa
- id (PK)
- nome_completo
- cpf (único)
- rg
- data_nascimento
- endereco
- bairro
- cidade
- estado
- cep
- telefone
- email
- pai_ou_mae (booleano)
- ajuda_hospital (booleano)
- ajuda_creche (booleano)
- recebeu_cesta_basica (booleano)
- participa_oficinas (booleano)
- interesse_novas_turmas (booleano)
- tem_filhos (booleano)
- ajuda_transporte (booleano)
- observacoes (texto)
- data_cadastro
- ultima_atualizacao

### MensagemPadrao
- id (PK)
- tipo (aniversario, dia_das_maes, dia_dos_pais, natal, ano_novo, outro)
- titulo
- conteudo
- ativa (booleano)
- data_criacao
- data_atualizacao

### DataComemorativa
- id (PK)
- nome
- data
- mensagem_id (FK -> MensagemPadrao)
- enviar_automaticamente (booleano)

### RegistroEnvioMensagem
- id (PK)
- pessoa_id (FK -> Pessoa)
- mensagem_id (FK -> MensagemPadrao)
- data_envio
- sucesso (booleano)
- observacao

## Relacionamentos

1. **DataComemorativa -> MensagemPadrao**
   - Relacionamento: N:1
   - Uma data comemorativa pode ter uma mensagem padrão associada
   - Uma mensagem padrão pode ser usada em várias datas comemorativas

2. **RegistroEnvioMensagem -> Pessoa**
   - Relacionamento: N:1
   - Um registro de envio está associado a uma pessoa
   - Uma pessoa pode ter vários registros de envio

3. **RegistroEnvioMensagem -> MensagemPadrao**
   - Relacionamento: N:1
   - Um registro de envio está associado a uma mensagem padrão
   - Uma mensagem padrão pode ter vários registros de envio

## Atributos Derivados

1. **Pessoa.idade()**
   - Calculado a partir da data_nascimento e data atual

2. **Pessoa.aniversario_hoje()**
   - Verifica se a pessoa faz aniversário na data atual

3. **Pessoa.aniversario_mes()**
   - Verifica se a pessoa faz aniversário no mês atual
