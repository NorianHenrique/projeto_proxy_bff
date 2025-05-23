# Projeto Proxy BFF (Backend for Frontend)
---

## Visão Geral

Este projeto implementa um Backend for Frontend (BFF). Utilizando o framework Flask em Python. Ele atua como uma camada intermediária (proxy) entre uma aplicação frontend 
e a API do backend, consolidando e adaptando as chamadas para otimizar a comunicação. O BFF centraliza a lógica de autenticação (obtenção e validação de tokens), tratamento de requisições e respostas, e fornece endpoints específicos para módulos como Funcionários, Clientes e Produtos.

---
## Status do Projeto

Em desenvolvimento

---

## Funcionalidades Principais

* **Autenticação Centralizada:** Gerencia a obtenção e renovação de tokens de acesso para APIs externas, garantindo que o frontend não precise lidar diretamente com a lógica de autenticação da API de backend.
* **Encaminhamento de Requisições:** Redireciona requisições do frontend para os endpoints apropriados das APIs de Funcionários, Clientes e Produtos.
* **Normalização de Respostas:** Processa e adapta as respostas das APIs de backend para um formato mais amigável ou otimizado para o frontend.
* **Módulo de Funcionários:** Oferece endpoints para listar, obter por ID, criar, atualizar (incluindo hash de senha) e deletar funcionários, além de verificar a existência de CPF e realizar login. As senhas são armazenadas com hash usando `bcrypt` para segurança.
* **Módulo de Clientes:** Implementa operações CRUD (Criar, Ler, Atualizar, Deletar) para clientes, incluindo validação de CPF.
* **Módulo de Produtos:** Permite listar, obter por ID, criar, atualizar e deletar produtos, com validação de nome.
* **Gerenciamento de Sessão:** Utiliza sessões Flask para armazenar dados como o token de acesso e seu tempo de validade.
* **Configuração Flexível:** Utiliza variáveis de ambiente (`.env`) para configurar URLs de APIs, portas, modo debug, credenciais de token e tempo de sessão, facilitando a implantação em diferentes ambientes.
* **CORS Configurado:** Permite requisições de origens específicas (definidas via `FRONTEND_URL`) para a API, garantindo a interoperabilidade com o frontend.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.x
* **Framework Web:** Flask
* **Bibliotecas Python:**
    * `Flask-CORS`: Para gerenciar as políticas de Cross-Origin Resource Sharing.
    * `python-dotenv`: Para carregar variáveis de ambiente de um arquivo `.env`.
    * `requests`: Para fazer requisições HTTP para as APIs de backend.
    * `bcrypt`: Para hash e verificação de senhas.
    * `blinker`, `certifi`, `charset-normalizer`, `click`, `colorama`, `idna`, `itsdangerous`, `Jinja2`, `MarkupSafe`, `urllib3`, `Werkzeug`: Dependências do Flask e do requests.
