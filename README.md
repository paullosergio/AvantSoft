# AvantSoft - API de Gestão de Clientes e Vendas

## Descrição

API RESTful para gerenciar clientes e suas compras, com autenticação JWT, estatísticas de vendas e testes automatizados. Desenvolvida com Django, Django REST Framework e PostgreSQL.

---

## 🚀 Como executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/paullosergio/AvantSoft.git
   cd AvantSoft
   ```

2. **Configure variáveis de ambiente**
   - O `docker-compose.yml` já define as principais variáveis para o banco.
   - Se usar `.env`, crie um arquivo com:
     ```env
     DB_NAME=toystore
     DB_USER=postgres
     DB_PASSWORD=postgres
     DB_HOST=db
     DB_PORT=5432
     SECRET_KEY=sua_secret_key
     DEBUG=True
     ```

3. **Suba os containers:**
   ```bash
   docker-compose up --build
   ```
   - O Django estará disponível em `http://localhost:8000`

4. **(Opcional) Crie um superusuário:**
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
   - Acesse o admin: [http://localhost:8000/admin/](http://localhost:8000/admin/)

---

## 🔐 Autenticação
- JWT obrigatório em todas as rotas.
- Obtenha o token em `POST /api/auth/`:
  ```json
  { "username": "seu_usuario", "password": "sua_senha" }
  ```
- Use o token nas requisições:
  ```
  Authorization: Bearer SEU_TOKEN
  ```

---

## 📚 Endpoints principais

### 👥 Clientes
- `GET /api/customers/` — Lista clientes (filtro: `?search=`)
- `POST /api/customers/` — Cria cliente
- `GET /api/customers/{id}/` — Detalhe
- `PUT/PATCH /api/customers/{id}/` — Atualiza
- `DELETE /api/customers/{id}/` — Remove

### 💰 Vendas
- `GET /api/sales/` — Lista vendas
- `POST /api/sales/` — Cria venda
- `GET /api/sales/{id}/` — Detalhe
- `PUT/PATCH /api/sales/{id}/` — Atualiza
- `DELETE /api/sales/{id}/` — Remove

### 📊 Estatísticas
- `GET /api/sales/stats/daily/` — Total de vendas por dia
- `GET /api/sales/stats/customers/` — Estatísticas por cliente:
  - Maior volume
  - Maior média
  - Maior frequência de compra

---

## 🧪 Testes

Rode todos os testes automatizados:
```bash
docker-compose exec web python manage.py test
```

---

## 🛠️ Exemplo de uso com curl

**Obter token:**
```bash
curl -X POST http://localhost:8000/api/auth/ -H "Content-Type: application/json" -d '{"username":"seu_usuario","password":"sua_senha"}'
```

**Criar cliente:**
```bash
curl -X POST http://localhost:8000/api/customers/ -H "Authorization: Bearer SEU_TOKEN" -H "Content-Type: application/json" -d '{"name":"João","email":"joao@exemplo.com","phone":"123456"}'
```

**Criar venda:**
```bash
curl -X POST http://localhost:8000/api/sales/ -H "Authorization: Bearer SEU_TOKEN" -H "Content-Type: application/json" -d '{"customer":1,"amount":"100.00","date":"2024-06-01"}'
```

**Estatísticas de vendas por dia:**
```bash
curl -X GET http://localhost:8000/api/sales/stats/daily/ -H "Authorization: Bearer SEU_TOKEN"
```

---

## 📦 Dependências principais
- Django
- djangorestframework
- djangorestframework-simplejwt
- psycopg2-binary
- python-decouple

---
