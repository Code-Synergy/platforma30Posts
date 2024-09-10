# Backend 30 Posts  

O sistema é uma plataforma de gestão integrada que automatiza e gerencia processos relacionados a 
clientes, ordens de serviço, formulários de captação de informações e geração de legendas para 
mídias sociais.  
Desenvolvido com o framework Flask e utilizando SQLAlchemy para gestão do banco de dados, o sistema 
organiza as operações em módulos independentes que se comunicam entre si, facilitando o fluxo de 
informações entre diferentes áreas de negócios.  
A plataforma também integra uma API externa para geração automatizada de conteúdo, oferecendo 
soluções personalizadas para os clientes e otimizando a criação de legendas para mídias sociais.  
Com autenticação baseada em tokens, o sistema garante segurança nas transações e eficiência na 
gestão dos dados, atendendo às necessidades de empresas que buscam digitalizar e automatizar seus 
processos internos.

## 🚀 Começando

Essas instruções permitirão que você obtenha uma cópia do projeto em operação na sua máquina local para fins de desenvolvimento e teste.

Consulte **[Implantação](#-implanta%C3%A7%C3%A3o)** para saber como implantar o projeto.

### 📋 Pré-requisitos

Para instalar e rodar o sistema, você precisará garantir que alguns pré-requisitos estejam atendidos e seguir as instruções de instalação descritas abaixo. Os principais pré-requisitos incluem o ambiente de desenvolvimento Python, ferramentas para gerenciamento de dependências, e um banco de dados PostgreSQL configurado.

1. Pré-requisitos Necessários: 
   Python 3.8+: Certifique-se de ter o Python instalado no seu sistema.  
   Você pode verificar se o Python está instalado executando o comando:

       python --version

   Se o Python não estiver instalado, faça o download e instale-o a partir do site oficial do Python.

2. PostgreSQL: Instale o PostgreSQL para gerenciar o banco de dados do 
   sistema. Certifique-se de que o servidor PostgreSQL esteja em execução e 
   crie um banco de dados específico para a aplicação:

       CREATE DATABASE seu_banco_de_dados;

   Você pode baixar o PostgreSQL no site oficial.

3. Pipenv ou Virtualenv: Utilizado para gerenciar o ambiente virtual e as 
   dependências do projeto. Instale com:

       pip install pipenv

   ou, se preferir o Virtualenv:

       pip install virtualenv

4. Git: Para clonar o repositório e gerenciar o controle de versão. 
   Instale o Git a partir do site oficial.
   Instruções de Instalação:
      Clone o Repositório do Projeto: Use o Git para clonar o repositório \
      do projeto na sua máquina local.

       git clone https://github.com/Code-Synergy/platforma30Posts.git
       cd seu_projeto

5. Configurar o Ambiente Virtual:
      Com Pipenv:

       pipenv install
       pipenv shell
      Com Virtualenv:

       python -m venv venv
       source venv/bin/activate  # No Windows: venv\Scripts\activate
       pip install -r requirements.txt

6. Configuração do Banco de Dados: No arquivo de configuração do projeto 
(config.py ou .env), configure as variáveis de ambiente relacionadas ao banco de dados:

       DATABASE_URL=postgresql://usuario:senha@localhost:5432/seu_banco_de_dados

   Inicialize o Banco de Dados: Execute as migrações para criar as tabelas no banco de dados.

       flask db init
       flask db migrate
       flask db upgrade

   Configure as Variáveis de Ambiente: Configure as variáveis essenciais, como FLASK_APP, FLASK_ENV, e as chaves de API necessárias.

       FLASK_APP=app.py
       FLASK_ENV=development
       JWT_SECRET_KEY=sua_chave_secreta
       OPENAI_API_KEY=sua_chave_openai
7. Execute o Servidor: Após concluir as configurações, você pode iniciar o 
servidor Flask.

       flask run

8. Testar a Aplicação: Utilize o Postman ou outra ferramenta de teste de 
API para verificar se os endpoints estão funcionando corretamente. Teste 
rotas de autenticação, criação de ordens de serviço, geração de legendas, 
entre outras.

9. Exemplo de Configuração de Produção:

   Usar Gunicorn para Servir a Aplicação:

       gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app

10. Configurar o Nginx como Proxy Reverso: No arquivo de configuração do 
Nginx, configure um proxy para o Gunicorn.

       server {
           listen 80;
           server_name seu_dominio.com;

        location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

    
## ⚙️ Executando os testes

Aqui estão os comandos curl para testar os principais endpoints de cada classe implementada no sistema:
1. Clientes (clientes.py)
   Registrar Cliente:

       curl -X POST "http://127.0.0.1:5000/clientes/" -H "Content-Type: application/json" -d '{"nome": "Cliente Teste", "email": "cliente@teste.com"}'
   Listar Clientes: 
       curl -X GET "http://127.0.0.1:5000/clientes/"

Atualizar Cliente:
          curl -X PUT "http://127.0.0.1:5000/clientes/1" -H "Content-Type: application/json" -d '{"nome": "Cliente Atualizado", "email": "cliente@teste.com"}'
   Deletar Cliente:

bash
Copiar código
curl -X DELETE "http://127.0.0.1:5000/clientes/1"
2. Formulário de Cliente (formulario_cliente.py)
Criar Formulário:

bash
Copiar código
curl -X POST "http://127.0.0.1:5000/formulario_cliente/" -H "Content-Type: application/json" -d '{"nome_formulario": "Formulário 1", "descricao": "Descrição do formulário"}'
Listar Formulários:

bash
Copiar código
curl -X GET "http://127.0.0.1:5000/formulario_cliente/"
Atualizar Formulário:

bash
Copiar código
curl -X PUT "http://127.0.0.1:5000/formulario_cliente/1" -H "Content-Type: application/json" -d '{"nome_formulario": "Formulário Atualizado"}'
Deletar Formulário:

bash
Copiar código
curl -X DELETE "http://127.0.0.1:5000/formulario_cliente/1"
3. Informações de Clientes (informacoes_clientes.py)
Adicionar Informação:

bash
Copiar código
curl -X POST "http://127.0.0.1:5000/informacoes_clientes/" -H "Content-Type: application/json" -d '{"cliente_id": 1, "informacao": "Nova informação"}'
Listar Informações:

bash
Copiar código
curl -X GET "http://127.0.0.1:5000/informacoes_clientes/"
Atualizar Informação:

bash
Copiar código
curl -X PUT "http://127.0.0.1:5000/informacoes_clientes/1" -H "Content-Type: application/json" -d '{"informacao": "Informação Atualizada"}'
Deletar Informação:

bash
Copiar código
curl -X DELETE "http://127.0.0.1:5000/informacoes_clientes/1"
4. Legendas (legendas.py)
Criar Legenda:

bash
Copiar código
curl -X POST "http://127.0.0.1:5000/legendas/" -H "Content-Type: application/json" -d '{"id_form": 1, "dia_post": 30, "ds_legenda": "Legenda de Teste"}'
Listar Legendas:

bash
Copiar código
curl -X GET "http://127.0.0.1:5000/legendas/"
Atualizar Legenda:

bash
Copiar código
curl -X PUT "http://127.0.0.1:5000/legendas/1" -H "Content-Type: application/json" -d '{"ds_legenda": "Legenda Atualizada"}'
Deletar Legenda:

bash
Copiar código
curl -X DELETE "http://127.0.0.1:5000/legendas/1"
5. Negócios (negocios.py)
Criar Negócio:

bash
Copiar código
curl -X POST "http://127.0.0.1:5000/negocios/" -H "Content-Type: application/json" -d '{"nome": "Negócio Teste"}'
Listar Negócios:

bash
Copiar código
curl -X GET "http://127.0.0.1:5000/negocios/"
Atualizar Negócio:

bash
Copiar código
curl -X PUT "http://127.0.0.1:5000/negocios/1" -H "Content-Type: application/json" -d '{"nome": "Negócio Atualizado"}'
Deletar Negócio:

bash
Copiar código
curl -X DELETE "http://127.0.0.1:5000/negocios/1"
6. Ordens de Serviço (ordens_de_servico.py)
Criar Ordem de Serviço:

bash
Copiar código
curl -X POST "http://127.0.0.1:5000/ordens_de_servico/" -H "Content-Type: application/json" -d '{"pedido_id": 1, "descricao": "Ordem Teste", "data": "2024-08-30", "usuario_id": 1, "workflow_id": 1}'
Listar Ordens de Serviço:

bash
Copiar código
curl -X GET "http://127.0.0.1:5000/ordens_de_servico/"
Atualizar Ordem de Serviço:

bash
Copiar código
curl -X PUT "http://127.0.0.1:5000/ordens_de_servico/1" -H "Content-Type: application/json" -d '{"descricao": "Ordem Atualizada"}'
Deletar Ordem de Serviço:

bash
Copiar código
curl -X DELETE "http://127.0.0.1:5000/ordens_de_servico/1"
7. Pedidos (pedido.py)
Criar Pedido:

bash
Copiar código
curl -X POST "http://127.0.0.1:5000/pedido/" -H "Content-Type: application/json" -d '{"cliente_id": 1, "descricao": "Pedido Teste"}'
Listar Pedidos:

bash
Copiar código
curl -X GET "http://127.0.0.1:5000/pedido/"
Atualizar Pedido:

bash
Copiar código
curl -X PUT "http://127.0.0.1:5000/pedido/1" -H "Content-Type: application/json" -d '{"descricao": "Pedido Atualizado"}'
Deletar Pedido:

bash
Copiar código
curl -X DELETE "http://127.0.0.1:5000/pedido/1"
8. Gepeto Zoe V3 (Gepeto_Zoe_V3.py)
Processar Legendas:

bash
Copiar código
curl -X POST "http://127.0.0.1:5000/zoe/" -H "Content-Type: application/json" -d '{"textao": "Texto de exemplo para geração de legenda."}'
Enviar Legenda:

bash
Copiar código
curl -X POST "http://127.0.0.1:5000/zoe/enviar_legenda" -H "Content-Type: application/json" -d '{"output": "Legenda gerada", "id_form": 1, "dia_post": 30}'
Esses comandos curl podem ser utilizados para testar os endpoints criados no backend do seu
Explicar como executar os testes automatizados para este sistema.


## 📦 Implantação

Configuração do Ambiente:

Requisitos: Certifique-se de que o servidor tenha Python 3.8 ou superior instalado, além de dependências como Flask, SQLAlchemy, e qualquer outra biblioteca especificada no arquivo requirements.txt.
Ambiente Virtual: Crie um ambiente virtual para isolar as dependências do projeto (python -m venv venv) e ative-o (source venv/bin/activate no Linux ou venv\Scripts\activate no Windows).
Instalação de Dependências: Instale todas as dependências necessárias usando pip install -r requirements.txt.
Configuração do Banco de Dados:

Configuração Inicial: Verifique as configurações de conexão com o banco de dados no arquivo de configuração do Flask (config.py ou semelhante). Ajuste as credenciais e parâmetros conforme o ambiente de produção.
Migração: Execute as migrações para configurar o esquema do banco de dados corretamente usando flask db upgrade.
Backup e Recuperação: Antes da implantação, faça backup do banco de dados atual. Tenha um plano de recuperação pronto para garantir que dados críticos não sejam perdidos.
Configuração de Variáveis de Ambiente:

Defina todas as variáveis de ambiente necessárias, como FLASK_APP, FLASK_ENV, JWT_SECRET_KEY, e credenciais para APIs externas (por exemplo, chave da OpenAI).
Configure as variáveis de ambiente para a produção para garantir que o sistema não opere no modo de depuração.
Implantação no Servidor:

Utilize um servidor de produção como Gunicorn ou uWSGI para servir a aplicação Flask. Evite usar o servidor de desenvolvimento do Flask em produção.
Configure um servidor web como Nginx ou Apache para fazer o proxy reverso do tráfego para o servidor da aplicação.
Certifique-se de que as portas necessárias estejam abertas e que as permissões estejam configuradas corretamente.
Segurança:

Autenticação e Autorização: Certifique-se de que todos os endpoints críticos estejam protegidos com autenticação JWT e que a lógica de autorização esteja devidamente implementada.
HTTPS: Implemente HTTPS para garantir que os dados transmitidos sejam seguros. Utilize certificados SSL/TLS válidos.
Firewall e Acesso: Configure um firewall para limitar o acesso ao sistema, permitindo apenas o tráfego necessário.
Monitoramento e Logs:

Configure o monitoramento de logs para capturar erros, acessos e eventos críticos do sistema. Utilize ferramentas como ELK Stack (Elasticsearch, Logstash, Kibana) ou serviços como Datadog.
Implemente alertas para notificá-lo sobre falhas no sistema ou comportamento anômalo.
Testes Pós-Implantação:

Realize testes de aceitação para garantir que todas as funcionalidades estejam operando conforme o esperado.
Teste a integração com sistemas externos, como APIs para geração de conteúdo, para garantir que a comunicação está fluindo corretamente.

## 🛠️ Construído com

Ferramentas e Tecnologias Utilizadas
Python 3.8+: Linguagem de programação principal utilizada para desenvolver o backend, com foco em facilidade de escrita, manutenção e integração com outras ferramentas.

Flask: Framework leve e versátil utilizado para criar a aplicação web. Facilitou a criação de rotas, manipulação de solicitações HTTP e integração com o banco de dados.

SQLAlchemy: Ferramenta de mapeamento objeto-relacional (ORM) usada para interagir com o banco de dados, facilitando a manipulação de dados e a criação de esquemas.

PostgreSQL: Banco de dados relacional utilizado para armazenar e gerenciar os dados do sistema, incluindo usuários, ordens de serviço, legendas e outras entidades.

Flask-CORS: Extensão do Flask utilizada para configurar Cross-Origin Resource Sharing (CORS), permitindo que o backend se comunique com diferentes origens, como frontends ou outros serviços.

JWT (JSON Web Token): Utilizado para autenticação e autorização dos usuários, garantindo a segurança das rotas e dados sensíveis do sistema.

OpenAI API: Utilizada para gerar conteúdo de legendas de forma automatizada e inteligente. A integração com a API permitiu adicionar funcionalidades avançadas de geração de texto.

Postman: Ferramenta utilizada para testar as APIs durante o desenvolvimento, garantindo que as requisições e respostas fossem tratadas corretamente.

GitHub: Utilizado para controle de versão do código, facilitando a colaboração e o rastreamento de alterações no projeto.

Gunicorn/uWSGI (para produção): Servidor de aplicação utilizado para servir a aplicação Flask em um ambiente de produção, garantindo desempenho e estabilidade.

Nginx/Apache (para proxy reverso): Servidores web utilizados para fazer proxy reverso, garantindo que as solicitações sejam gerenciadas de forma eficiente e segura.

VS Code/PyCharm: IDEs (Ambientes de Desenvolvimento Integrado) utilizadas para o desenvolvimento do código, com suporte para depuração, auto-completar e outras funcionalidades que aumentam a produtividade.

Docker (opcional): Utilizado para criar containers que isolam a aplicação e suas dependências, facilitando a implantação em diferentes ambientes de forma consistente.

## 🖇️ Colaborando

Por favor, leia o [COLABORACAO.md](https://gist.github.com/usuario/linkParaInfoSobreContribuicoes) para obter detalhes sobre o nosso código de conduta e o processo para nos enviar pedidos de solicitação.

## 📌 Versão

Nós usamos [SemVer](http://semver.org/) para controle de versão. Para as versões disponíveis, observe as [tags neste repositório](https://github.com/suas/tags/do/projeto). 

## ✒️ Autores

Mencione todos aqueles que ajudaram a levantar o projeto desde o seu início

* **Um desenvolvedor** - *Trabalho Inicial* - [umdesenvolvedor](https://github.com/linkParaPerfil)
* **Fulano De Tal** - *Documentação* - [fulanodetal](https://github.com/linkParaPerfil)

Você também pode ver a lista de todos os [colaboradores](https://github.com/usuario/projeto/colaboradores) que participaram deste projeto.

## 📄 Licença

Este projeto está sob a licença (sua licença) - veja o arquivo [LICENSE.md](https://github.com/usuario/projeto/licenca) para detalhes.

## 🎁 Expressões de gratidão

* Conte a outras pessoas sobre este projeto 📢;
* Convide alguém da equipe para uma cerveja 🍺;
* Um agradecimento publicamente 🫂;
* etc.


---
⌨️ com ❤️ por [Armstrong Lohãns](https://gist.github.com/lohhans) 😊