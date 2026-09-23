# Gestão de Contatos

Sistema web para **gestão e consulta de contactos telefónicos internos**, desenvolvido com **Python, FastAPI e PostgreSQL**.

A aplicação permite consultar funcionários, departamentos e respetivas extensões telefónicas. Utilizadores autenticados com permissões de administração podem adicionar, editar e eliminar contactos.

---

## Funcionalidades

* Consulta de contactos telefónicos
* Pesquisa por:

  * Nome do funcionário
  * Departamento
  * Extensão
* Filtro por departamento
* Paginação dos resultados
* Visualização do número total de contactos
* Autenticação de administrador
* Criação de token JWT
* Adição de novos contactos
* Edição de contactos
* Eliminação de contactos
* Prevenção de extensões duplicadas
* Gestão automática de departamentos
* Interface web integrada com FastAPI
* API REST para operações de contactos

---

## Tecnologias utilizadas

### Backend

* Python
* FastAPI
* Uvicorn
* PostgreSQL
* psycopg2
* Pydantic
* JWT
* bcrypt

### Frontend

* HTML5
* CSS3
* JavaScript
* Font Awesome
* Google Fonts

---

## Estrutura do projeto

```text
site_gestao_telefone/
│
├── main.py                 # Aplicação principal FastAPI
├── database.py             # Ligação à base de dados PostgreSQL
├── auth.py                 # Autenticação, passwords e JWT
├── crud.py                 # Operações CRUD
├── models.py               # Modelos da aplicação
├── schemas.py              # Schemas Pydantic
├── create_user.py          # Script para criar utilizador administrador
├── resize.py               # Script auxiliar
│
├── routers/
│   └── contatos.py         # Rotas da API de contactos
│
├── frontend/
│   ├── index.html          # Interface web
│   └── static/
│       └── iconeContatos.png
│
└── requirements.txt        # Dependências Python
```

---

# Requisitos

Antes de executar o projeto, é necessário ter instalado:

* Python 3.10 ou superior
* PostgreSQL
* pip
* Git (opcional)

## 3. Instalar as dependências

Execute:

```bash
pip install -r requirements.txt
```
---

# Criar utilizador administrador

Depois de configurar a base de dados, execute:

```bash
python create_user.py
```

O script cria o utilizador administrativo configurado no ficheiro `create_user.py`.

> Por motivos de segurança, altere as credenciais antes de utilizar a aplicação em produção.

---

# Executar o projeto

```bash
uvicorn main:app --reload
```

Se tudo estiver correto, deverá aparecer algo semelhante a:

```text
Uvicorn running on http://127.0.0.1:8000
```

A aplicação estará disponível em:

```text
http://127.0.0.1:8000
```

---

# Documentação da API

O FastAPI disponibiliza automaticamente a documentação interativa.

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---


Este projeto é de utilização interna. A definição de uma licença específica poderá ser adicionada posteriormente conforme a necessidade da organização.
