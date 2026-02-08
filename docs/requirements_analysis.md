# Análise de Requisitos — FinancePlus

**Autor:** Tharles Freitas
**Data:** 04/11/2025  
**Versão:** 1.0

🧭 Contexto do Sistema

O sistema é um aplicativo de controle financeiro pessoal, que permite aos usuários registrar suas despesas e receitas, visualizar relatórios e acompanhar o saldo disponível.
Ele será acessível via web e dispositivos móveis (no futuro), com banco de dados SQLite inicialmente.

🎯 Objetivo

Fornecer uma ferramenta simples e acessível para ajudar o usuário a controlar suas finanças pessoais, planejar gastos e visualizar onde o dinheiro está sendo utilizado.

👥 Atores

Usuário: pessoa que usa o sistema para gerenciar suas finanças (cria conta, adiciona despesas, etc.).

(Opcional futuramente) Administrador: gerencia usuários, categorias globais ou relatórios gerais.

📋 Requisitos Funcionais (RF)

São as funcionalidades que o sistema deve ter.

🔐 Autenticação

RF01 – O sistema deve permitir o cadastro de novos usuários.

RF02 – O sistema deve permitir login e logout de usuários.

RF03 – O sistema deve proteger rotas que exigem autenticação.

💰 Despesas e Receitas

RF04 – O sistema deve permitir cadastrar novas despesas (valor, categoria, data, descrição).

RF05 – O sistema deve permitir cadastrar receitas.

RF06 – O sistema deve permitir editar ou excluir uma despesa/receita.

RF07 – O sistema deve listar todas as despesas e receitas do usuário autenticado.

RF08 – O sistema deve calcular o saldo atual (receitas - despesas).

🏷️ Categorias

RF09 – O usuário pode criar e gerenciar suas próprias categorias.

RF10 – O sistema deve permitir filtrar despesas por categoria e/ou período.

📊 Relatórios

RF11 – O sistema deve exibir gráficos ou relatórios resumidos com totais mensais.

RF12 – O sistema deve permitir exportar relatórios (CSV, PDF — futuro).

⚙️ Requisitos Não Funcionais (RNF)

São as qualidades técnicas que o sistema precisa ter.

RNF01 – O sistema deve ser desenvolvido em Python 3.10+.

RNF02 – O framework backend deve ser FastAPI.

RNF03 – O banco de dados inicial será SQLite, com possibilidade de migração para PostgreSQL.

RNF04 – O código deve seguir o padrão PEP8 e passar pelos linters black, isort, pylint.

RNF05 – A API deve seguir boas práticas REST.

RNF06 – O sistema deve ser facilmente implantável via Render ou Railway.

RNF07 – O tempo de resposta das requisições deve ser inferior a 2 segundos.

RNF08 – Os dados sensíveis devem ser armazenados de forma segura (hash de senha com bcrypt ou passlib).

🧩 Casos de Uso (resumo)

Cadastrar usuário

Fazer login

Cadastrar despesa/receita

Editar/Excluir despesa

Visualizar lista de despesas

Filtrar despesas por categoria/período

Gerar relatório mensal

Visualizar saldo atual
