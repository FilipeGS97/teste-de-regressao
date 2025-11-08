# teste-de-regressao
Testes de regressão em sites.

🌐 **Testes End-to-End (E2E) do Frontend com Selenium**
Este repositório contém um script de automação E2E desenvolvido em Python com a biblioteca Selenium WebDriver, focado em garantir a navegabilidade e a funcionalidade básica do website.

🎯 **Objetivo**
O principal objetivo do teste é simular a jornada completa de um usuário, desde a navegação como visitante (deslogado) até o acesso e interação com as áreas restritas (logado), garantindo que todos os elementos e fluxos críticos estejam funcionando corretamente.

O script reporta erros no arquivo test_site_errors.log e no console, permitindo a identificação imediata de funcionalidades quebradas.

⚙️ **Pré-requisitos**
Para executar este script, você precisará ter instalado:

- Python 3.x
- Biblioteca selenium (pip install selenium)
- Um WebDriver compatível com o navegador de sua escolha (ex: ChromeDriver, GeckoDriver). O binário do driver deve estar acessível no PATH do sistema ou especificado no código.
- Credenciais de teste válidas para as variáveis EMAIL_LOGIN e SENHA_LOGIN.

🗺️ **Cobertura e Fluxo de Teste**
O script simula mais de 125 passos de usuário, cobrindo os seguintes fluxos principais:

**1. Navegação como Visitante (Deslogado)**
- Acesso e Interação com Modais: Teste de abertura e fechamento dos modais de Login e Registro (via cabeçalho e menu inferior).
- Verificação da Homepage: Validação da exibição de elementos chave, como Banner Principal, Categorias de Jogos e Footer.
- Navegação de Jogos: Teste dos links do Menu Inferior (Crash Games, Exclusivos, Home) e funcionalidade de Pesquisa de jogos dentro das categorias.

**2. Autenticação**
Fluxo de Login: Simulação da entrada de EMAIL_LOGIN e SENHA_LOGIN e clique no botão de Entrar.

**3. Funções Transacionais (Logado)**
- Fluxo de Depósito: Navegação para a tela de Depósito (via cabeçalho), preenchimento do Valor e clique para confirmar (etapas de confirmação final e QR Code estão comentadas para evitar transações reais).
- Fluxo de Saque: Navegação para a tela de Saque, preenchimento do Valor e clique em Solicitar Saque (etapas finais comentadas).
- Volta para a Home: Verificação de que o usuário retorna corretamente para a página principal após as operações.

**4. Navegação na Área do Usuário (Menu Perfil/Configurações)**
O script navega e verifica a exibição de elementos em todas as subseções da área do usuário, garantindo o carregamento correto das telas de gerenciamento:

- **Perfil:** Minha Conta, Informações Pessoais, Dados Bancários, Endereço, Senha, Avatar, Limites.
- **Outras Seções:** Documentos, Saldo, Bônus, Depósito (via área do usuário), Solicitar Saque (via área do usuário).
- **Históricos:** Pedidos de Saques, Histórico de Depósitos, Transações de Cassino.

**5. Finalização**
Logout: Simulação do clique em Sair e da confirmação de saída do sistema.

📝 **Relatório de Erros**
Todas as falhas de interação (ex: elemento não encontrado, elemento não clicável, timeout) são registradas pelo sistema de log personalizado:

- **Saída no Console:** Mensagens de ERRO LOGADO são exibidas em tempo real.
- **Arquivo de Log:** Um arquivo chamado test_site_errors.log é criado ou sobrescrito a cada execução, contendo o timestamp, a descrição da falha e o XPATH do elemento que causou o problema.
- **Captura de Tela:** Em caso de um ERRO CRÍTICO (não tratado), o script tenta salvar uma captura de tela para auxiliar na depuração.

⚠️ **Observação Importante**
Todos os XPATHs e URLs no script (ex: URL_DO_SITE, XPATH_QRCODE_DEPOSITO, SEU_XPATH_AQUI) são dados de exemplo e devem ser substituídos pelos valores reais do ambiente de teste para que a automação funcione corretamente.
