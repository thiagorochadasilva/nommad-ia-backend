# AI Platform Backend

Este é o back-end da plataforma de IA, desenvolvido em Flask com integração à API Gemini do Google.

## Funcionalidades

- **Chat com IA**: Endpoint para conversar com a IA usando a API Gemini
- **Histórico de Conversas**: Armazenamento e recuperação do histórico de conversas por usuário
- **CORS habilitado**: Permite requisições do front-end
- **Health Check**: Endpoint para verificar se o serviço está funcionando

## Endpoints da API

### Chat
- **POST** `/api/chat`
  - Envia uma mensagem para a IA e recebe uma resposta
  - Body: `{"message": "sua mensagem", "user_id": "id_do_usuario"}`
  - Response: `{"response": "resposta da IA", "user_id": "id", "status": "success"}`

### Histórico de Conversa
- **GET** `/api/conversation/<user_id>`
  - Obtém o histórico de conversa de um usuário
  - Response: `{"user_id": "id", "conversation": [...], "message_count": 10}`

- **DELETE** `/api/conversation/<user_id>`
  - Limpa o histórico de conversa de um usuário
  - Response: `{"message": "Conversa limpa", "status": "success"}`

### Health Check
- **GET** `/api/health`
  - Verifica se o serviço está funcionando
  - Response: `{"status": "healthy", "service": "AI Platform Backend", "version": "1.0.0"}`

## Configuração

1. Ative o ambiente virtual:
   ```bash
   source venv/bin/activate
   ```

2. Configure a chave da API Gemini:
   ```bash
   export GEMINI_API_KEY=sua_chave_aqui
   ```

3. Execute o servidor:
   ```bash
   python src/main.py
   ```

O servidor estará disponível em `http://localhost:5000`

## Dependências

- Flask: Framework web
- Flask-CORS: Suporte a CORS
- Flask-SQLAlchemy: ORM para banco de dados
- requests: Cliente HTTP para chamadas à API Gemini

## Estrutura do Projeto

```
src/
├── models/          # Modelos de dados
├── routes/          # Rotas da API
│   ├── ai.py       # Rotas relacionadas à IA
│   └── user.py     # Rotas de usuário (template)
├── static/         # Arquivos estáticos
├── database/       # Banco de dados SQLite
└── main.py         # Ponto de entrada da aplicação
```

