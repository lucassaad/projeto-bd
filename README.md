# Hospital System — Project Architecture

Este documento descreve a arquitetura, organização e propósito de cada diretório do projeto.  
Ele serve como referência para entendimento do design, manutenção e evolução do sistema.

---

# 📁 Estrutura de Diretórios

```
hospital_system/
│
├── app/
│   ├── api/                     # Rotas da aplicação (controllers)
│   ├── services/                # Regras de negócio
│   ├── repositories/            # Camada de persistência (acesso ao BD)
│   ├── models/                  # SQLAlchemy ORM (tabelas)
│   ├── schemas/                 # Pydantic (validação e DTOs)
│   ├── db/                      # Configuração de banco de dados
│   ├── core/                    # Configurações gerais
│   ├── main.py                  # Ponto inicial da aplicação FastAPI
├── tests/                       # Testes automatizados
├── requirements.txt             # Dependências da aplicação
├── README.md                    # Documentação principal
├── .env                         # Variáveis de ambiente
└── .gitignore
```

---

# 🧱 Arquitetura em Camadas

A aplicação segue o padrão **Layered Architecture**:

```
Rotas (API)       → app/api/
Serviços          → app/services/
Repositórios      → app/repositories/
ORM / Models      → app/models/
Banco de Dados    → PostgreSQL
```

### ✔ API (Rotas)
Contém apenas:
- definições de endpoints
- validação de entrada via Pydantic
- chamadas para a camada de serviços

Nenhuma regra de negócio é colocada aqui.

---

### ✔ Services (Regras de Negócio)
Implementa:
- validações complexas
- regras de negócio
- lógica entre diferentes entidades
- chamadas aos repositórios

Os services **não conhecem SQLAlchemy diretamente** — apenas o repository layer.

---

### ✔ Repositories (Persistência)
Responsável por:
- CRUD no banco
- queries SQL via SQLAlchemy ORM
- abstrair o acesso ao banco da camada de serviço

Isso isola totalmente o SQLAlchemy do restante do sistema.

---

### ✔ Models (ORM)
Classes que representam tabelas do banco usando SQLAlchemy ORM.

---

### ✔ Schemas (Pydantic)
Usados para:
- validação
- entrada/saída em rotas
- prevenção de exposição direta de modelos ORM

---

### ✔ DB (Configuração de Banco)
Contém:
- criação do engine
- SessionLocal
- inicialização do banco

---

# 🚀 main.py

O arquivo `main.py` cria a aplicação FastAPI e registra todos os roteadores:

```python
from fastapi import FastAPI
from app.api.patients import router as patient_router
from app.api.doctors import router as doctor_router
from app.api.appointments import router as appointment_router

app = FastAPI(title="Hospital System API")

app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)
```

---

# 🎯 Objetivo da Arquitetura

A estrutura foi projetada para garantir:

- **Alta separação de responsabilidades**
- **Código limpo e fácil de manter**
- **Baixo acoplamento entre camadas**
- **Escalabilidade**
- **Fácil entendimento para correção e expansão**
- **Aderência a boas práticas de mercado**

---

# 📌 Como navegar

| Diretório       | Função |
|-----------------|--------|
| `api/`          | Endpoints REST |
| `services/`     | Regras de negócio |
| `repositories/` | Operações no banco |
| `models/`       | ORM do SQLAlchemy |
| `schemas/`      | Pydantic DTOs |
| `db/`           | Configuração de banco |
| `core/`         | Configurações globais |
| `tests/`        | Testes automatizados |

---
