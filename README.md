# FinancePlus API

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-green)
![Poetry](https://img.shields.io/badge/Poetry-Managed-blueviolet)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen)

**FinancePlus** é uma API REST robusta para gestão financeira pessoal. Oferece autenticação segura via JWT, gestão de categorias e rastreamento de transações, desenvolvida com foco em **Clean Architecture**, **Escalabilidade** e **Boas Práticas**.

---

## ✨ Funcionalidades

- **Autenticação Segura**: Login e proteção de rotas via JWT.
- **Gestão de Usuários**: Cadastro e perfil de usuários.
- **Controle Financeiro**: Gerenciamento de receitas e despesas.
- **Categorização**: Organização de transações por categorias personalizadas.
- **Stack Moderna**: Construído com Flask, SQLAlchemy, Pydantic e Flasgger.

---

## � Como Começar

### Pré-requisitos

- **Python 3.10+**
- **Poetry** (Gerenciador de Dependências)

### Instalação

1. **Instalar Dependências**
   ```bash
   poetry install
   ```

2. **Configurar Ambiente**
   Crie o arquivo `.env` na raiz do projeto:
   ```bash
   cp .env.example .env
   ```

3. **Executar Aplicação**
   ```bash
   poetry run flask run
   ```

---

## 🧪 Testes

O projeto utiliza **Pytest** para testes de integração abrangentes.

```bash
poetry run pytest
```

---

## 🏗️ Arquitetura

O projeto segue uma arquitetura em camadas para garantir separação de responsabilidades e manutenibilidade.

```
src/app/
├── controllers/    # Rotas e Manipuladores de Requisição
├── services/       # Regras de Negócio
├── repositories/   # Acesso a Dados
├── models/         # Entidades do Banco de Dados
└── schemas/        # Validação de Dados (Pydantic)
```

---

Desenvolvido com 💜 por Tharlesdev
