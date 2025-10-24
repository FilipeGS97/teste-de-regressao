# O intuito do teste é acessar todas as páginas do front e testar suas principais funções, reportando erro das que não funcionem corretamente. 

import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException

# --- ARQUIVO DE LOG E LISTA DE ERROS ---
LOG_FILE = "test_site_errors.log"
test_errors_list = []  # Para manter uma lista de erros na memória

# --- CONFIGURAÇÕES INICIAIS ---
URL_DO_SITE = "https://site.exemplo.com/BR"  # Substitua pela URL do seu site
EMAIL_LOGIN = "teste123@gmail.com"       # Substitua pelo seu e-mail de teste
SENHA_LOGIN = "teste123$#"          # Substitua pela sua senha de teste
VALOR_DEPOSITO_TESTE = "5"                # Valor para o campo de depósito
VALOR_SAQUE_TESTE = "5"                    # Valor para o campo de saque

# --- XPATHs DOS ELEMENTOS ---
# Obs: Substitua "SEU_XPATH_AQUI" pelos XPATHs reais dos elementos no seu site.

# Elementos Gerais e Menu Lateral
XPATH_BOTAO_MENU_LATERAL = "//*[@id='__nuxt']/div/main/header/div[1]/button"
XPATH_ELEMENTO_VISIVEL_NO_MENU = "//*[@id='__nuxt']/div/main/div[1]/aside/div[1]/p"
XPATH_BOTAO_FECHAR_MENU_LATERAL = "//*[@id='__nuxt']/div/main/header/div[1]/button"

# Modal Login/Registro (Cabeçalho)
XPATH_BOTAO_LOGIN_CABECALHO = "//*[@id='__nuxt']/div/main/header/div[2]/button[1]"
XPATH_MODAL_LOGIN = "//*[@id='login']"
XPATH_BOTAO_FECHAR_MODAL_LOGIN = "//*[@id='__nuxt']/div/main/div[2]/button"
XPATH_BOTAO_REGISTRO_CABECALHO = "//*[@id='__nuxt']/div/main/header/div[2]/button[2]"
XPATH_MODAL_REGISTRO = "//*[@id='__nuxt']/div/main/div[2]/div/div/div/div/form/label[1]"
XPATH_BOTAO_FECHAR_MODAL_REGISTRO = "//*[@id='__nuxt']/div/main/div[2]/button"

# Elementos da Página Principal (Deslogado)
XPATH_BANNER_PRINCIPAL = "//*[@id='carousel-banner-']/div[2]/div[1]/a/img"
XPATH_BOTOES_CATEGORIAS = "//*[@id='__nuxt']/div/main/div[1]/div/div[2]"
XPATH_CATEGORIA_EXCLUSIVOS_PRINCIPAL = "//*[@id='exclusivos']/div[1]/div/h2/span"
XPATH_CATEGORIA_MAIS_JOGADOS_PRINCIPAL = "//*[@id='mais-jogados']/div[1]/div/h2/span"
XPATH_CATEGORIA_CRASH_GAMES_PRINCIPAL = "//*[@id='crash-games']/div[1]/div/h2/span"
XPATH_CATEGORIA_COMPRAR_RODADAS_PRINCIPAL = "//*[@id='comprar-rodadas']/div[1]/div/h2/span"
XPATH_FOOTER = "//*[@id='__nuxt']/div/main/div[1]/footer/div/div[1]"

# Menu Inferior e Navegação (Deslogado)
XPATH_BOTAO_CRASH_GAMES_MENU_INFERIOR = "//*[@id='__nuxt']/div/main/nav/ul/li[2]/a"
XPATH_NOME_CRASH_GAMES_TOPO = "//*[@id='__nuxt']/div/main/div[1]/div/div/div/div[1]/div[1]/span"
XPATH_BARRA_PESQUISA_CRASH_GAMES = "//*[@id='search']"
XPATH_LOGO_JOGO_BUFFALO_CRASH = "//*[@id='__nuxt']/div/main/div[1]/div/div/div/div[2]/div/a/img"

XPATH_BOTAO_COMEÇAR_MENU_INFERIOR = "//*[@id='__nuxt']/div/main/nav/ul/li[1]/a" # Home
XPATH_ICONE_CATEGORIA_EXCLUSIVOS_HOME = "//*[@id='__nuxt']/div/main/div/div/div[2]/div/ul/li[1]/a" # Verificação após clicar em Começar

XPATH_BOTAO_EXCLUSIVOS_MENU_INFERIOR = "//*[@id='__nuxt']/div/main/nav/ul/li[3]/a"
XPATH_NOME_EXCLUSIVOS_TOPO = "//*[@id='__nuxt']/div/main/div/div/div/div/div[1]/div[1]/span"
XPATH_BARRA_PESQUISA_EXCLUSIVOS = "//*[@id='search']"
XPATH_LOGO_JOGO_BIRD_EXCLUSIVOS = "//*[@id='__nuxt']/div/main/div/div/div/div/div[2]/div/a/img"

XPATH_BOTAO_LOGIN_MENU_INFERIOR = "//*[@id='__nuxt']/div/main/nav/ul/li[4]/button"
XPATH_MODAL_LOGIN_MENU_INFERIOR = "//*[@id='login']"
XPATH_BOTAO_FECHAR_MODAL_LOGIN_MENU_INFERIOR = "//*[@id='__nuxt']/div/main/div[2]/button"

XPATH_BOTAO_REGISTRO_MENU_INFERIOR = "//*[@id='__nuxt']/div/main/nav/ul/li[5]/button"
XPATH_MODAL_REGISTRO_MENU_INFERIOR = "//*[@id='document']"
XPATH_BOTAO_FECHAR_MODAL_REGISTRO_MENU_INFERIOR = "//*[@id='__nuxt']/div/main/div[2]/button"

# Formulário de Login
XPATH_CAMPO_EMAIL_LOGIN = "//*[@id='login']"
XPATH_CAMPO_SENHA_LOGIN = "//*[@id='password']"
XPATH_BOTAO_LOGIN_ENTRAR_MODAL = "//*[@id='__nuxt']/div/main/div[2]/div/div/div/div/form/button[1]"

# Depósito
XPATH_BOTAO_DEPOSITO_APOS_LOGIN = "//*[@id='__nuxt']/div/main/header/div[2]/div[2]/button"
XPATH_NOME_DEPOSITO_TOPO = "//*[@id='__nuxt']/div/main/header/div/span"
XPATH_CAMPO_VALOR_DEPOSITO = "//*[@id='__nuxt']/div/main/div/div/div[2]/div/div[2]/div/div[1]/div[1]/input"
XPATH_BOTAO_DEPOSITAR_CONFIRMAR = "//*[@id='__nuxt']/div/main/div/div/div[2]/div/div[2]/div/div[3]"
XPATH_QRCODE_DEPOSITO = "SEU_XPATH_AQUI_QRCODE_DEPOSITO"
XPATH_BOTAO_VOLTAR_TOPO_DEPOSITO = "//*[@id='__nuxt']/div/main/header/div/button"

# Ícone Exclusivos na Página Inicial (para verificação após voltar de depósito/saque)
XPATH_ICONE_EXCLUSIVOS_PAGINA_INICIAL_LOGADO = "//*[@id='__nuxt']/div/main/div/div/div[2]/div/ul/li[1]/a" # Usado após voltar de depósito/saque

# Saque
XPATH_BOTAO_SETA_EXIBIR_SAQUE = "//*[@id='__nuxt']/div/main/header/div[2]/div[2]/div/button" # Pode ser um botão de perfil/menu de usuário
XPATH_BOTAO_SAQUE = "//*[@id='__nuxt']/div/main/header/div[2]/div[2]/div/ul/li/button"
XPATH_NOME_SAQUE_TOPO = "//*[@id='__nuxt']/div/main/header/div/span"
XPATH_CAMPO_VALOR_SAQUE = "//*[@id='amount']"
XPATH_BOTAO_SOLICITAR_SAQUE = "//*[@id='root-container']/form/button"
XPATH_MENSAGEM_ERRO_SAQUE = "SEU_XPATH_AQUI_MENSAGEM_ERRO_SAQUE" # Verificar se erro é exibido
XPATH_BOTAO_VOLTAR_TOPO_SAQUE = "//*[@id='__nuxt']/div/main/header/div/button"

# Elementos da Página Principal (Logado)
XPATH_BANNER_PRINCIPAL_LOGADO = "//*[@id='carousel-banner-']/div[2]/div[1]/a/img"
XPATH_BOTOES_CATEGORIAS_LOGADO = "//*[@id='__nuxt']/div/main/div/div/div[2]"
XPATH_CATEGORIA_EXCLUSIVOS_PRINCIPAL_LOGADO = "//*[@id='exclusivos']/div[1]/div/h2/span"
XPATH_CATEGORIA_MAIS_JOGADOS_PRINCIPAL_LOGADO = "//*[@id='mais-jogados']/div[1]/div/h2/span"
XPATH_CATEGORIA_CRASH_GAMES_PRINCIPAL_LOGADO = "//*[@id='crash-games']/div[1]/div/h2/span"
XPATH_CATEGORIA_COMPRAR_RODADAS_PRINCIPAL_LOGADO = "//*[@id='comprar-rodadas']/div[1]/div/h2/span"
XPATH_FOOTER_LOGADO = "//*[@id='__nuxt']/div/main/div/footer/div/div[1]"

# Menu Inferior e Navegação (Logado)
XPATH_BOTAO_CRASH_GAMES_MENU_INFERIOR_LOGADO = "//*[@id='__nuxt']/div/main/nav/ul/li[2]/a"
XPATH_NOME_CRASH_GAMES_TOPO_LOGADO = "//*[@id='__nuxt']/div/main/div/div/div/div/div[1]/div[1]/span"
XPATH_BARRA_PESQUISA_CRASH_GAMES_LOGADO = "//*[@id='search']"
XPATH_LOGO_JOGO_BUFFALO_CRASH_LOGADO = "//*[@id='__nuxt']/div/main/div/div/div/div/div[2]/div/a/img"

XPATH_BOTAO_COMEÇAR_MENU_INFERIOR_LOGADO = "//*[@id='__nuxt']/div/main/nav/ul/li[1]/a" # Home
XPATH_ICONE_CATEGORIA_EXCLUSIVOS_HOME_LOGADO = "//*[@id='__nuxt']/div/main/div/div/div[2]/div/ul/li[1]/a"

XPATH_BOTAO_EXCLUSIVOS_MENU_INFERIOR_LOGADO = "//*[@id='__nuxt']/div/main/nav/ul/li[3]/a"
XPATH_NOME_EXCLUSIVOS_TOPO_LOGADO = "//*[@id='__nuxt']/div/main/div/div/div/div/div[1]/div[1]/span"
XPATH_BARRA_PESQUISA_EXCLUSIVOS_LOGADO = "//*[@id='search']"
XPATH_LOGO_JOGO_BIRD_EXCLUSIVOS_LOGADO = "//*[@id='__nuxt']/div/main/div/div/div/div/div[2]/div/a/img"

# Menu Usuário / Perfil (Logado)
XPATH_BOTAO_USUARIO_MENU_INFERIOR = "//*[@id='__nuxt']/div/main/nav/ul/li[4]/a" # Botão que leva para a área do usuário/perfil
XPATH_ID_USUARIO_VISIVEL = "//*[@id='__nuxt']/div/main/div/div/div/div/p[2]/span[1]" # Verificação inicial na tela do usuário
XPATH_LINK_PERFIL = "//*[@id='__nuxt']/div/main/div/div/ul/li[1]/a"
XPATH_NOME_PERFIL_TOPO = "//*[@id='__nuxt']/div/main/header/div/span"

XPATH_LINK_MINHA_CONTA = "//*[@id='__nuxt']/div/main/div/div/div/div/div/div/div[1]"
XPATH_NOME_ID_USUARIO_MINHA_CONTA = "//*[@id='collapse-option-account']/div/div[2]/div/p[1]/span"
XPATH_TEMPO_UTILIZACAO_HOJE = "//*[@id='collapse-option-account']/div/div[2]/div/p[4]/span"
XPATH_TOTAL_ACUMULADO = "//*[@id='collapse-option-account']/div/div[2]/div/p[7]/span"

XPATH_LINK_INFORMACOES_PESSOAIS = "//*[@id='__nuxt']/div/main/div/div/div/div/div/div/div[3]"
XPATH_NOME_COMPLETO_INFO_PESSOAIS = "//*[@id='collapse-option-personal']/div[1]/label"
XPATH_DATA_NASCIMENTO_INFO_PESSOAIS = "//*[@id='collapse-option-personal']/div[3]/label"
XPATH_NOME_USUARIO_INFO_PESSOAIS = "//*[@id='collapse-option-personal']/div[6]/label"

XPATH_LINK_DADOS_BANCARIOS = "//*[@id='__nuxt']/div/main/div/div/div/div/div/div/div[5]"
XPATH_CPF_DADOS_BANCARIOS = "//*[@id='collapse-option-bank']/div/div/div[2]/div[1]/div[1]/p/span"

XPATH_LINK_ENDERECO = "//*[@id='__nuxt']/div/main/div/div/div/div/div/div/div[7]"
XPATH_RUA_ENDERECO = "//*[@id='collapse-option-address']/div[3]/label"

XPATH_LINK_SENHA = "//*[@id='__nuxt']/div/main/div/div/div/div/div/div/div[9]"
XPATH_SENHA_ATUAL_CAMPO_TEXTO = "//*[@id='collapse-option-password']/div[1]/label" # Geralmente é um label ou texto próximo

XPATH_LINK_AVATAR = "//*[@id='__nuxt']/div/main/div/div/div/div/div/div/div[11]"
XPATH_TEXTO_ESCOLHA_AVATAR = "//*[@id='collapse-option-avatar']/div/p"

XPATH_LINK_LIMITES = "//*[@id='__nuxt']/div/main/div/div/div/div/div/div/div[13]"
XPATH_TEXTO_NOVO_LIMITE_APOSTAS = "//*[@id='collapse-option-limits']/div/div[2]/h5"

XPATH_BOTAO_VOLTAR_TOPO_PERFIL = "//*[@id='__nuxt']/div/main/header/div/button" # Volta da tela de perfil para a tela anterior (menu usuário)

XPATH_BOTAO_DOCUMENTOS = "//*[@id='__nuxt']/div/main/div/div/ul/li[2]/a"
XPATH_ELEMENTO_PROCESSO_VERIFICACAO = "//*[@id='documents-collapse']/div[2]"
XPATH_BOTAO_VOLTAR_TOPO_DOCUMENTOS = "//*[@id='__nuxt']/div/main/header/div/button" # Volta da tela de documentos

XPATH_BOTAO_SALDO = "//*[@id='__nuxt']/div/main/div/div/ul/li[3]/a"
XPATH_ELEMENTO_VISIVEL_SALDO = "//*[@id='__nuxt']/div/main/div/div/div/div[2]/div[2]/div[1]/span" # Adicionado para verificação
XPATH_BOTAO_VOLTAR_TOPO_SALDO = "//*[@id='__nuxt']/div/main/header/div/button" # Adicionado para navegação

XPATH_BOTAO_BONUS = "//*[@id='__nuxt']/div/main/div/div/ul/li[4]/a"
XPATH_ELEMENTO_BONUS_ATIVOS = "//*[@id='__nuxt']/div/main/div/div/div/div[2]/button[1]/span[1]"
XPATH_BOTAO_VOLTAR_TOPO_BONUS = "//*[@id='__nuxt']/div/main/header/div/button"

XPATH_BOTAO_DEPOSITO_AREA_USUARIO = "//*[@id='__nuxt']/div/main/div/div/ul/li[5]/a" # Se for diferente do XPATH_BOTAO_DEPOSITO_APOS_LOGIN
XPATH_ELEMENTO_CODIGO_BONUS = "//*[@id='__nuxt']/div/main/div/div/div[2]/div/div[2]/div/div[2]/label"
XPATH_BOTAO_VOLTAR_TOPO_DEPOSITO_AREA_USUARIO = "//*[@id='__nuxt']/div/main/header/div/button"

XPATH_BOTAO_SOLICITAR_SAQUE_AREA_USUARIO = "//*[@id='__nuxt']/div/main/div/div/ul/li[6]/a" # Se for diferente do XPATH_BOTAO_SAQUE
XPATH_ELEMENTO_SELECIONE_CHAVE_PIX = "//*[@id='root-container']/form/span"
XPATH_BOTAO_VOLTAR_TOPO_SAQUE_AREA_USUARIO = "//*[@id='__nuxt']/div/main/header/div/button"

XPATH_BOTAO_PEDIDOS_DE_SAQUES = "//*[@id='__nuxt']/div/main/div/div/ul/li[7]/a"
XPATH_ELEMENTO_TIPO_TRANSACAO = "//*[@id='__nuxt']/div/main/div/div/div[3]/div/table/thead/tr/th[2]"
XPATH_BOTAO_VOLTAR_TOPO_PEDIDOS_DE_SAQUES = "//*[@id='__nuxt']/div/main/header/div/button"

XPATH_BOTAO_HISTORICO_DE_DEPOSITOS = "//*[@id='__nuxt']/div/main/div/div/ul/li[8]/a"
XPATH_ELEMENTO_DATA_HORA_HISTORICO_DEPOSITOS = "//*[@id='__nuxt']/div/main/div/div/div[3]/div/table/thead/tr/th[1]"
XPATH_BOTAO_VOLTAR_TOPO_HISTORICO_DE_DEPOSITOS = "//*[@id='__nuxt']/div/main/header/div/button"

XPATH_BOTAO_TRANSACOES_DE_CASSINO = "//*[@id='__nuxt']/div/main/div/div/ul/li[9]/a"
XPATH_ELEMENTO_BONUS_ID_APOSTA = "//*[@id='__nuxt']/div/main/div/div/div[2]/table/thead/tr/th[1]"
XPATH_BOTAO_VOLTAR_TOPO_TRANSACOES_DE_CASSINO = "//*[@id='__nuxt']/div/main/header/div/button"

XPATH_BOTAO_SAIR = "//*[@id='__nuxt']/div/main/div/div/ul/li[10]/button"
XPATH_ELEMENTO_LEMBRETE_SAIR = "//*[@id='__nuxt']/div/main/div/div/div[2]/div/div/div/h3"
XPATH_BOTAO_CONFIRMAR_SAIDA= "//*[@id='__nuxt']/div/main/div/div/div[2]/div/div/div/div/button[1]"

# --- FUNÇÕES DE LOG ---
def log_error(descricao_passo, xpath_ou_variavel, detalhes_erro):
    """Registra uma mensagem de erro no arquivo de log e na lista de erros."""
    global test_errors_list
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    mensagem_erro_console = f"ERRO LOGADO: {descricao_passo} | Elemento/Variável: {xpath_ou_variavel} | Detalhes: {str(detalhes_erro)[:200]}" # Limita o tamanho da msg de erro no console
    print(mensagem_erro_console)

    mensagem_erro_arquivo = f"[{timestamp}] ERRO: {descricao_passo}\n"
    mensagem_erro_arquivo += f"  Elemento/Variável: {xpath_ou_variavel}\n"
    mensagem_erro_arquivo += f"  Detalhes: {str(detalhes_erro)}\n---\n"
    
    test_errors_list.append(mensagem_erro_arquivo)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(mensagem_erro_arquivo)

def iniciar_log():
    """Escreve um cabeçalho no arquivo de log para uma nova execução de teste."""
    global test_errors_list
    test_errors_list = [] # Limpa a lista de erros para a nova execução
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    header = f"\n{'='*70}\nINÍCIO DO TESTE AUTOMATIZADO: {timestamp}\n{'='*70}\n"
    with open(LOG_FILE, 'w', encoding='utf-8') as f: # 'w' para sobrescrever o log a cada nova execução
        f.write(header)
    print(f"Log de erros iniciado. As falhas serão salvas em: {LOG_FILE}")

def finalizar_log():
    """Escreve um rodapé no arquivo de log."""
    if not test_errors_list:
        mensagem_final = "Nenhum erro registrado durante o teste.\n"
    else:
        mensagem_final = f"{len(test_errors_list)} erro(s) registrado(s) durante o teste. Consulte {LOG_FILE} para detalhes.\n"
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    footer = f"\n{'='*70}\nFIM DO TESTE AUTOMATIZADO: {timestamp}\n{mensagem_final}{'='*70}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(footer)
    print(mensagem_final)

# --- FUNÇÕES AUXILIARES DE INTERAÇÃO COM SELENIUM (COM LOG) ---
def aguardar_e_clicar_com_log(driver, by, value, descricao_acao, espera=10):
    """Espera um elemento ficar clicável, clica nele e registra erros sem parar o script."""
    try:
        elemento = WebDriverWait(driver, espera).until(EC.element_to_be_clickable((by, value)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", elemento)
        time.sleep(0.3)
        elemento.click()
        print(f"SUCESSO: Clicado em '{descricao_acao}' (XPATH: {value})")
        return True
    except Exception as e:
        log_error(f"Falha ao clicar em '{descricao_acao}'", value, e)
        return False

def verificar_elemento_exibido_com_log(driver, by, value, descricao_elemento, espera=10):
    """Verifica se um elemento está sendo exibido e registra erros sem parar o script."""
    try:
        elemento = WebDriverWait(driver, espera).until(EC.visibility_of_element_located((by, value)))
        if elemento.is_displayed():
            print(f"SUCESSO: Elemento '{descricao_elemento}' (XPATH: {value}) está sendo exibido.")
            return True
        else:
            log_error(f"Elemento '{descricao_elemento}' localizado mas não visível (is_displayed()=false)", value, "Elemento encontrado mas is_displayed() retornou False")
            return False
    except Exception as e:
        log_error(f"Elemento '{descricao_elemento}' não encontrado ou não ficou visível", value, e)
        return False

def preencher_campo_com_log(driver, by, value, texto, descricao_campo, espera=10):
    """Preenche um campo de formulário e registra erros sem parar o script."""
    try:
        elemento = WebDriverWait(driver, espera).until(EC.visibility_of_element_located((by, value)))
        driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'center'});", elemento)
        time.sleep(0.3)
        elemento.clear()
        elemento.send_keys(texto)
        print(f"SUCESSO: Preenchido campo '{descricao_campo}' (XPATH: {value}) com '{texto}'")
        return True
    except Exception as e:
        log_error(f"Falha ao preencher o campo '{descricao_campo}'", value, e)
        return False

def rolar_para_fim_da_pagina(driver, descricao_pagina="Página Atual"):
    """Rola a página até o final."""
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1) 
        print(f"SUCESSO: Rolado até o fim da {descricao_pagina}.")
        return True
    except Exception as e:
        log_error(f"Falha ao rolar para o fim da {descricao_pagina}", "N/A", e)
        return False

# --- SCRIPT DE TESTE PRINCIPAL ---
def executar_teste():
    # Configurar o WebDriver (exemplo com Chrome)
    # Certifique-se de que o chromedriver está no seu PATH ou especifique o caminho:
    # options = webdriver.ChromeOptions()
    # options.add_argument('--headless') # Para rodar sem interface gráfica (opcional)
    # driver = webdriver.Chrome(executable_path='/caminho/para/o/chromedriver', options=options)
    driver = webdriver.Chrome() # Ou webdriver.Firefox(), webdriver.Edge(), etc.
    driver.maximize_window()
    
    iniciar_log()

    try:
        # PASSO 1: Acessar a URL
        print("\n--- PASSO 1: Acessando URL ---")
        try:
            driver.get(URL_DO_SITE)
            print(f"SUCESSO: Acessada a URL: {URL_DO_SITE}")
        except Exception as e:
            log_error("Falha crítica ao acessar a URL inicial", URL_DO_SITE, e)
            print("Não foi possível carregar a URL inicial. O teste será interrompido.")
            return # Interrompe se a URL base não carregar

        # PASSO 2: Aguardar 3 segundos
        print("Aguardando 3 segundos...")
        time.sleep(3)

        # PASSO 3: Clicar em um botão [Botão menu lateral]
        print("\n--- Interagindo com Menu Lateral ---")
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_MENU_LATERAL, "Botão menu lateral")

        # PASSO 4: Aguardar 3 segundos
        time.sleep(3)

        # PASSO 5: Verificar se um elemento é exibido
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ELEMENTO_VISIVEL_NO_MENU, "Elemento no menu lateral")

        # PASSO 6: Clicar em um botão [Botão fechar menu lateral]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_FECHAR_MENU_LATERAL, "Botão fechar menu lateral")
        time.sleep(1) 

        print("\n--- Interagindo com Modais de Login/Registro (Cabeçalho) ---")
        # PASSO 7: Clicar em um botão [Botão login] (do cabeçalho)
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_LOGIN_CABECALHO, "Botão Login (cabeçalho)")

        # PASSO 8: Verificar se um elemento é exibido [Modal login]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_MODAL_LOGIN, "Modal de Login (cabeçalho)")

        # PASSO 9: Clicar em um botão [X de fechar modal login]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_FECHAR_MODAL_LOGIN, "Botão fechar Modal Login (cabeçalho)")
        time.sleep(1)

        # PASSO 10: Clicar em um botão [Botão registro] (do cabeçalho)
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_REGISTRO_CABECALHO, "Botão Registro (cabeçalho)")

        # PASSO 11: Verificar se um elemento é exibido [Modal registro]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_MODAL_REGISTRO, "Modal de Registro (cabeçalho)")

        # PASSO 12: Clicar em um botão [X de fechar modal registro]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_FECHAR_MODAL_REGISTRO, "Botão fechar Modal Registro (cabeçalho)")
        time.sleep(1)

        print("\n--- Verificando Elementos da Página Principal (Deslogado) ---")
        # PASSO 13: Verificar se um elemento está sendo exibido [banner]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_BANNER_PRINCIPAL, "Banner principal (deslogado)")
        # PASSO 14: Verificar se um elemento está sendo exibido [botões de categorias]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_BOTOES_CATEGORIAS, "Botões de categorias (deslogado)")
        # PASSO 15: Verificar se um elemento está sendo exibido [categoria exclusivos da página principal]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_CATEGORIA_EXCLUSIVOS_PRINCIPAL, "Categoria Exclusivos (principal - deslogado)")
        # PASSO 16: Verificar se um elemento está sendo exibido [categoria mais-jogados da página principal]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_CATEGORIA_MAIS_JOGADOS_PRINCIPAL, "Categoria Mais Jogados (principal - deslogado)")
        # PASSO 17: Verificar se um elemento está sendo exibido [categoria crash-games da página principal]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_CATEGORIA_CRASH_GAMES_PRINCIPAL, "Categoria Crash Games (principal - deslogado)")
        # PASSO 18: Verificar se um elemento está sendo exibido [categoria comprar-rodadas da página principal]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_CATEGORIA_COMPRAR_RODADAS_PRINCIPAL, "Categoria Comprar Rodadas (principal - deslogado)")

        # PASSO 19: ROLAR ATÉ O FIM DA PÁGINA [PÁGINA PRINCIPAL]
        rolar_para_fim_da_pagina(driver, "Página Principal (deslogado)")
        # PASSO 20: Verificar se um elemento está sendo exibido [Footer]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_FOOTER, "Footer (deslogado)")

        print("\n--- Navegação via Menu Inferior (Deslogado) ---")
        # PASSO 21: Clicar em um elemento [Botão Crash Games do menu inferior]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_CRASH_GAMES_MENU_INFERIOR, "Botão Crash Games (menu inferior - deslogado)")
        time.sleep(2) 
        # PASSO 22: Verificar se um elemento é exibido [Nome Crash Games no topo]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_NOME_CRASH_GAMES_TOPO, "Nome Crash Games no topo (deslogado)")
        # PASSO 23: Digitar o nome "buffalo" na barra de pesquisa [Barra de pesquisa da categoria Crash Games]
        preencher_campo_com_log(driver, By.XPATH, XPATH_BARRA_PESQUISA_CRASH_GAMES, "buffalo", "Barra de pesquisa Crash Games (deslogado)")
        time.sleep(1) 
        # PASSO 24: Verificar se um elemento é exibido [Logo do jogo]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_LOGO_JOGO_BUFFALO_CRASH, "Logo do jogo 'buffalo' em Crash Games (deslogado)")

        # PASSO 25: Clicar em um elemento [Botão Começar do menu inferior] (Voltar para Home)
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_COMEÇAR_MENU_INFERIOR, "Botão Começar/Home (menu inferior - deslogado)")
        time.sleep(2)
        # PASSO 26: Verificar se um elemento é exibido [ícone da categoria Exclusivos] (na home, após voltar)
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ICONE_CATEGORIA_EXCLUSIVOS_HOME, "Ícone da categoria Exclusivos na Home (deslogado)")

        # PASSO 27: Clicar em um elemento [Botão Exclusivos do menu inferior]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_EXCLUSIVOS_MENU_INFERIOR, "Botão Exclusivos (menu inferior - deslogado)")
        time.sleep(2)
        # PASSO 28: Verificar se um elemento é exibido [Nome Exclusivos no topo]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_NOME_EXCLUSIVOS_TOPO, "Nome Exclusivos no topo (deslogado)")
        # PASSO 29: Digitar o nome "Bird" na barra de pesquisa [Barra de pesquisa da categoria Exclusivos]
        preencher_campo_com_log(driver, By.XPATH, XPATH_BARRA_PESQUISA_EXCLUSIVOS, "Bird", "Barra de pesquisa Exclusivos (deslogado)")
        time.sleep(1)
        # PASSO 30: Verificar se um elemento é exibido [Logo do jogo]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_LOGO_JOGO_BIRD_EXCLUSIVOS, "Logo do jogo 'Bird' em Exclusivos (deslogado)")

        print("\n--- Interagindo com Modais de Login/Registro (Menu Inferior) ---")
        # PASSO 31: Clicar em um botão [Botão login do menu inferior]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_LOGIN_MENU_INFERIOR, "Botão Login (menu inferior)")
        # PASSO 32: Verificar se um elemento é exibido [Modal login do menu inferior]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_MODAL_LOGIN_MENU_INFERIOR, "Modal de Login (menu inferior)")
        # PASSO 33: Clicar em um botão [X de fechar modal login do menu inferior]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_FECHAR_MODAL_LOGIN_MENU_INFERIOR, "Botão fechar Modal Login (menu inferior)")
        time.sleep(1)

        # PASSO 34: Clicar em um botão [Botão registro do menu inferior]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_REGISTRO_MENU_INFERIOR, "Botão Registro (menu inferior)")
        # PASSO 35: Verificar se um elemento é exibido [Modal registro do menu inferior]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_MODAL_REGISTRO_MENU_INFERIOR, "Modal de Registro (menu inferior)")
        # PASSO 36: Clicar em um botão [X de fechar modal registro do menu inferior]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_FECHAR_MODAL_REGISTRO_MENU_INFERIOR, "Botão fechar Modal Registro (menu inferior)")
        time.sleep(1)

        print("\n--- INICIANDO FLUXO DE LOGIN ---")
        # PASSO 37: Clicar em um botão [Botão login do menu inferior] (para abrir o modal de login novamente)
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_LOGIN_MENU_INFERIOR, "Botão Login (menu inferior) para logar")
        time.sleep(1) 
        # PASSO 38: Preencher o formulário E-mail [Campo E-mail login]
        preencher_campo_com_log(driver, By.XPATH, XPATH_CAMPO_EMAIL_LOGIN, EMAIL_LOGIN, "Campo E-mail login")
        # PASSO 39: Preencher o formulário Senha [Campo Senha login]
        preencher_campo_com_log(driver, By.XPATH, XPATH_CAMPO_SENHA_LOGIN, SENHA_LOGIN, "Campo Senha login")
        # PASSO 40: Clicar em um botão [Botão Login/Entrar do modal login]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_LOGIN_ENTRAR_MODAL, "Botão Login/Entrar (modal)")
        # PASSO 41: Aguardar 5 segundos (para o login processar e a página carregar)
        print("Aguardando 5 segundos para processamento do login...")
        time.sleep(5)
        print("Login supostamente realizado. Verificações de estado logado a seguir.")

        # PASSO 42: Clicar em um elemento [Botão Começar do menu inferior] (para ir para a home logado)
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_COMEÇAR_MENU_INFERIOR_LOGADO, "Botão Começar/Home (menu inferior - logado)") 
        time.sleep(2)

        print("\n--- INICIANDO FLUXO DE DEPÓSITO ---")
        # PASSO 43: Clicar em um botão [Botão depósito]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_DEPOSITO_APOS_LOGIN, "Botão Depósito (após login)")
        time.sleep(2)
        # PASSO 44: Verificar se um elemento é exibido [Nome depósito no topo]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_NOME_DEPOSITO_TOPO, "Título 'Depósito' no topo")

        # --- Seção de Depósito Comentada ---
        # print("\n--- SEÇÃO DE DEPÓSITO (COMENTADA NO SCRIPT ORIGINAL) ---")
        # # PASSO 45: Preencher campo formulário [Campo valor de depósito]
        # preencher_campo_com_log(driver, By.XPATH, XPATH_CAMPO_VALOR_DEPOSITO, VALOR_DEPOSITO_TESTE, "Campo valor de depósito")
        # # PASSO 46: Clicar em um botão [Botão depósito/depositar]
        # aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_DEPOSITAR_CONFIRMAR, "Botão Confirmar Depósito")
        # time.sleep(3) 
        # # PASSO 47: Verificar se um elemento é exibido [QRCode]
        # verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_QRCODE_DEPOSITO, "QRCode de depósito")
        # --- Fim da Seção Comentada ---

        # PASSO 48: Clicar em um botão [Seta de voltar no topo de depósito]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_DEPOSITO, "Botão Voltar (tela de Depósito)")
        time.sleep(2) 
        # PASSO 49: Verificar se um elemento é exibido [Ícone Exclusivos da página inicial]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ICONE_EXCLUSIVOS_PAGINA_INICIAL_LOGADO, "Ícone Exclusivos na página inicial (após voltar de depósito)")

        print("\n--- INICIANDO FLUXO DE SAQUE ---")
        # PASSO 50: Clicar em um botão [Seta para exibir botão Saque] (ou botão de perfil/menu de usuário)
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_SETA_EXIBIR_SAQUE, "Botão Menu Usuário/Seta para Saque")
        time.sleep(1) 
        # PASSO 51: Clicar em um botão [Botão saque]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_SAQUE, "Botão Saque")
        time.sleep(2) 
        # PASSO 52: Verificar se um elemento é exibido [Nome saque no topo]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_NOME_SAQUE_TOPO, "Título 'Saque' no topo")

        # --- Seção de Saque Comentada ---
        # print("\n--- SEÇÃO DE SAQUE (COMENTADA NO SCRIPT ORIGINAL) ---")
        # # PASSO 53: Preencher campo formulário [Campo valor de saque]
        # preencher_campo_com_log(driver, By.XPATH, XPATH_CAMPO_VALOR_SAQUE, VALOR_SAQUE_TESTE, "Campo valor de saque")
        # # PASSO 54: Clicar em um botão [Botão Solicitar saque]
        # aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_SOLICITAR_SAQUE, "Botão Solicitar Saque")
        # time.sleep(3)
        # # PASSO 55: Verificar se um elemento é exibido [Ver se erro é exibido]
        # verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_MENSAGEM_ERRO_SAQUE, "Mensagem de erro/sucesso no saque")
        # --- Fim da Seção Comentada ---

        # PASSO 56: Clicar em um botão [Seta de voltar no topo de saque]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_SAQUE, "Botão Voltar (tela de Saque)")
        time.sleep(2)
        # PASSO 57: Verificar se um elemento é exibido [Ícone Exclusivos da página inicial]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ICONE_EXCLUSIVOS_PAGINA_INICIAL_LOGADO, "Ícone Exclusivos na página inicial (após voltar de saque)")

        print("\n--- Verificando Elementos da Página Principal (Logado) ---")
        # PASSO 58: Verificar se um elemento está sendo exibido [banner - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_BANNER_PRINCIPAL_LOGADO, "Banner principal (logado)")
        # PASSO 59: Verificar se um elemento está sendo exibido [botões de categorias - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_BOTOES_CATEGORIAS_LOGADO, "Botões de categorias (logado)")
        # PASSO 60: Verificar se um elemento está sendo exibido [categoria exclusivos da página principal - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_CATEGORIA_EXCLUSIVOS_PRINCIPAL_LOGADO, "Categoria Exclusivos (principal - logado)")
        # PASSO 61: Verificar se um elemento está sendo exibido [categoria mais-jogados da página principal - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_CATEGORIA_MAIS_JOGADOS_PRINCIPAL_LOGADO, "Categoria Mais Jogados (principal - logado)")
        # PASSO 62: Verificar se um elemento está sendo exibido [categoria crash-games da página principal - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_CATEGORIA_CRASH_GAMES_PRINCIPAL_LOGADO, "Categoria Crash Games (principal - logado)")
        # PASSO 63: Verificar se um elemento está sendo exibido [categoria comprar-rodadas da página principal - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_CATEGORIA_COMPRAR_RODADAS_PRINCIPAL_LOGADO, "Categoria Comprar Rodadas (principal - logado)")
        # PASSO 64: ROLAR ATÉ O FIM DA PÁGINA [PÁGINA PRINCIPAL]
        rolar_para_fim_da_pagina(driver, "Página Principal (logado)")
        # PASSO 65: Verificar se um elemento está sendo exibido [Footer - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_FOOTER_LOGADO, "Footer (logado)")

        print("\n--- Navegação via Menu Inferior (Logado) ---")
        # PASSO 66: Clicar em um elemento [Botão Crash Games do menu inferior - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_CRASH_GAMES_MENU_INFERIOR_LOGADO, "Botão Crash Games (menu inferior - logado)")
        time.sleep(2)
        # PASSO 67: Verificar se um elemento é exibido [Nome Crash Games no topo - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_NOME_CRASH_GAMES_TOPO_LOGADO, "Nome Crash Games no topo (logado)")
        # PASSO 68: Digitar o nome "buffalo" na barra de pesquisa [Barra de pesquisa da categoria Crash Games - logado]
        preencher_campo_com_log(driver, By.XPATH, XPATH_BARRA_PESQUISA_CRASH_GAMES_LOGADO, "buffalo", "Barra de pesquisa Crash Games (logado)")
        time.sleep(1)
        # PASSO 69: Verificar se um elemento é exibido [Logo do jogo - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_LOGO_JOGO_BUFFALO_CRASH_LOGADO, "Logo do jogo 'buffalo' em Crash Games (logado)")

        # PASSO 70: Clicar em um elemento [Botão Começar do menu inferior - logado] (Voltar para Home)
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_COMEÇAR_MENU_INFERIOR_LOGADO, "Botão Começar/Home (menu inferior - logado)")
        time.sleep(2)
        # PASSO 71: Verificar se um elemento é exibido [ícone da categoria Exclusivos - logado] (na home)
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ICONE_CATEGORIA_EXCLUSIVOS_HOME_LOGADO, "Ícone da categoria Exclusivos na Home (logado)")

        # PASSO 72: Clicar em um elemento [Botão Exclusivos do menu inferior - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_EXCLUSIVOS_MENU_INFERIOR_LOGADO, "Botão Exclusivos (menu inferior - logado)")
        time.sleep(2)
        # PASSO 73: Verificar se um elemento é exibido [Nome Exclusivos no topo - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_NOME_EXCLUSIVOS_TOPO_LOGADO, "Nome Exclusivos no topo (logado)")
        # PASSO 74: Digitar o nome "Bird" na barra de pesquisa [Barra de pesquisa da categoria Exclusivos - logado]
        preencher_campo_com_log(driver, By.XPATH, XPATH_BARRA_PESQUISA_EXCLUSIVOS_LOGADO, "Bird", "Barra de pesquisa Exclusivos (logado)")
        time.sleep(1)
        # PASSO 75: Verificar se um elemento é exibido [Logo do jogo - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_LOGO_JOGO_BIRD_EXCLUSIVOS_LOGADO, "Logo do jogo 'Bird' em Exclusivos (logado)")

        print("\n--- NAVEGAÇÃO ÁREA DO USUÁRIO / PERFIL ---")
        # PASSO 76: Clicar em um elemento [Botão Usuário do menu inferior - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_USUARIO_MENU_INFERIOR, "Botão Usuário (menu inferior - logado)")
        time.sleep(2) 
        # PASSO 77: Verificar se um elemento é exibido [ID do usuário - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ID_USUARIO_VISIVEL, "ID do usuário (tela de usuário)")

        # PASSO 78: Clicar em um elemento [Clica em Perfil - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_LINK_PERFIL, "Link/Botão Perfil")
        time.sleep(2)
        # PASSO 79: Verificar se um elemento é exibido [Nome Perfil no topo - logado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_NOME_PERFIL_TOPO, "Título 'Perfil' no topo")

        print("\n  --- Subseções do Perfil ---")
        # PASSO 80: Clicar em um elemento [Clica em Minha conta - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_LINK_MINHA_CONTA, "Link/Botão Minha Conta")
        time.sleep(1)
        # PASSO 81: Verificar se um elemento é exibido [Nome ID do usuário]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_NOME_ID_USUARIO_MINHA_CONTA, "ID do usuário (Minha Conta)")
        # PASSO 82: Verificar se um elemento é exibido [Nome Tempo de utilização do site hoje]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_TEMPO_UTILIZACAO_HOJE, "Tempo de utilização (Minha Conta)")
        # PASSO 83: Verificar se um elemento é exibido [Nome Total acumulado]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_TOTAL_ACUMULADO, "Total acumulado (Minha Conta)")

        # PASSO 84: Clicar em um elemento [Clica em Informações Pessoais - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_LINK_INFORMACOES_PESSOAIS, "Link/Botão Informações Pessoais")
        time.sleep(1)
        # PASSO 85: Verificar se um elemento é exibido [Nome Nome completo]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_NOME_COMPLETO_INFO_PESSOAIS, "Nome completo (Informações Pessoais)")
        # PASSO 86: Verificar se um elemento é exibido [Nome Data de Nascimento]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_DATA_NASCIMENTO_INFO_PESSOAIS, "Data de Nascimento (Informações Pessoais)")
        # PASSO 87: Verificar se um elemento é exibido [Nome Nome de usuário]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_NOME_USUARIO_INFO_PESSOAIS, "Nome de usuário (Informações Pessoais)")

        # PASSO 88: Clicar em um elemento [Clica em Dados bancários - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_LINK_DADOS_BANCARIOS, "Link/Botão Dados Bancários")
        time.sleep(1)
        # PASSO 89: Verificar se um elemento é exibido [Nome CPF]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_CPF_DADOS_BANCARIOS, "CPF (Dados Bancários)")

        # PASSO 90: Clicar em um elemento [Clica em Endereço - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_LINK_ENDERECO, "Link/Botão Endereço")
        time.sleep(1)
        # PASSO 91: Verificar se um elemento é exibido [Nome Rua]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_RUA_ENDERECO, "Rua (Endereço)")

        # PASSO 92: Clicar em um elemento [Clica em Senha - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_LINK_SENHA, "Link/Botão Senha")
        time.sleep(1)
        # PASSO 93: Verificar se um elemento é exibido [Nome Senha atual]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_SENHA_ATUAL_CAMPO_TEXTO, "Label 'Senha atual' (Senha)")

        # PASSO 94: Clicar em um elemento [Clica em Avatar - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_LINK_AVATAR, "Link/Botão Avatar")
        time.sleep(1)
        # PASSO 95: Verificar se um elemento é exibido [Nome Escolha o seu avatar]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_TEXTO_ESCOLHA_AVATAR, "Texto 'Escolha o seu avatar'")

        # PASSO 96: Clicar em um elemento [Clica em Limites - logado]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_LINK_LIMITES, "Link/Botão Limites")
        time.sleep(1)
        # PASSO 97: Verificar se um elemento é exibido [Nome Inserir um novo limite de apostas]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_TEXTO_NOVO_LIMITE_APOSTAS, "Texto 'Inserir um novo limite de apostas'")

        # PASSO 98: Clicar em um botão [Seta de voltar no topo de Perfil]
        # Este botão volta da subseção (Limites) para a tela principal de Perfil, ou da tela de Perfil para o menu de usuário?
        # Ajuste o XPATH. Assumindo que volta para a tela de "Perfil" onde tem os links para subseções.

        # Agora, para voltar da tela de "Perfil" para o "Menu do Usuário" (onde clicou em Documentos/Saldo)
        # Pode ser o mesmo botão XPATH_BOTAO_VOLTAR_TOPO_PERFIL ou outro. Ajuste se necessário.
        # Se o botão anterior já voltou para o "Menu do Usuário", este clique pode não ser necessário ou dar erro.
        # Supondo que o XPATH_BOTAO_VOLTAR_TOPO_PERFIL é o botão da página de perfil principal que volta pro menu do usuário:
        # Se o passo 98 levou para a listagem de Perfil (Minha Conta, Info Pessoais etc),
        # então precisaria de um botão para voltar dessa listagem para o menu de usuário antes de clicar em Documentos.
        # Ou, se o XPATH_LINK_PERFIL levou a uma página que contém todas as subseções E o botão de voltar para o menu de usuário
        # então o XPATH_BOTAO_VOLTAR_TOPO_PERFIL seria esse.
        # Para simplificar, vamos assumir que o PASSO 98 levou para uma tela que ainda é "dentro" do perfil,
        # e precisamos de mais um "voltar" para acessar "Documentos" e "Saldo" como irmãos de "Perfil".
        # Se "Documentos" e "Saldo" estão DENTRO de "Perfil" como sub-itens, a lógica de navegação seria diferente.
        # Vou seguir a lógica que "Perfil", "Documentos" e "Saldo" são acessados a partir de um mesmo "Menu do Usuário".
        # O PASSO 78 clicou em Perfil. O PASSO 98 clicou em voltar DENTRO de perfil. 
        # Para clicar em Documentos, precisa voltar da TELA DE PERFIL para o MENU DE USUÁRIO.
        # Este XPATH_BOTAO_VOLTAR_TOPO_PERFIL deve ser o botão que faz isso.
        print("\n  --- Voltando para Menu do Usuário e acessando outras seções ---")
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_PERFIL, "Botão Voltar (da tela de Perfil para Menu do Usuário)")
        time.sleep(2)
        
        # PASSO 99: Clicar em um botão [Clicar em Documentos]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_DOCUMENTOS, "Link/Botão Documentos")
        time.sleep(5)
        # PASSO 100: Verificar se um elemento é exibido [Elemento Processo de Verificação]
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ELEMENTO_PROCESSO_VERIFICACAO, "Elemento 'Processo de Verificação' (Documentos)")
        # PASSO 101: Clicar em um botão [Seta de voltar no topo de Documentos]
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_DOCUMENTOS, "Botão Voltar (tela de Documentos para Menu do Usuário)")
        time.sleep(2) 

        # PASSO 102: Clicar em um botão [Clicar em Saldo] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_SALDO, "Link/Botão Saldo")
        time.sleep(2)
        # PASSO 103: Verificar se um elemento é exibido [Elemento Saldo do usuário] 
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ELEMENTO_VISIVEL_SALDO, "Elemento Saldo do usuário")
        # PASSO 104: Clicar em um botão [Seta de voltar no topo de Saldo] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_SALDO, "Botão Voltar (tela de Saldo)")
        time.sleep(2)

        # PASSO 105: Clicar em um botão [Clicar em Bônus] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_BONUS, "Link/Botão Bônus")
        time.sleep(2)
        # PASSO 106: Verificar se um elemento é exibido [Elemento Bônus ativos] 
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ELEMENTO_BONUS_ATIVOS, "Elemento Bônus ativos")
        # PASSO 107: Clicar em um botão [Seta de voltar no topo de Bônus] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_BONUS, "Botão Voltar (tela de Bônus)")
        time.sleep(2)

        # PASSO 108: Clicar em um botão [Clicar em Depósito] 
        # Usando um novo XPATH_BOTAO_DEPOSITO_AREA_USUARIO para o botão de depósito dentro da área do usuário
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_DEPOSITO_AREA_USUARIO, "Link/Botão Depósito (Área do Usuário)")
        time.sleep(2)
        # PASSO 109: Verificar se um elemento é exibido [Elemento Código de Bônus] 
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ELEMENTO_CODIGO_BONUS, "Elemento Código de Bônus (Depósito na Área do Usuário)")
        # PASSO 110: Clicar em um botão [Seta de voltar no topo de Depósito] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_DEPOSITO_AREA_USUARIO, "Botão Voltar (tela de Depósito na Área do Usuário)")
        time.sleep(2)

        # PASSO 111: Clicar em um botão [Clicar em Solicitar saque] 
        # Usando um novo XPATH_BOTAO_SOLICITAR_SAQUE_AREA_USUARIO para o botão de saque dentro da área do usuário
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_SOLICITAR_SAQUE_AREA_USUARIO, "Link/Botão Solicitar Saque (Área do Usuário)")
        time.sleep(2)
        # PASSO 112: Verificar se um elemento é exibido [Elemento Selecione a chave pix] 
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ELEMENTO_SELECIONE_CHAVE_PIX, "Elemento Selecione a chave pix (Saque na Área do Usuário)")
        # PASSO 113: Clicar em um botão [Seta de voltar no topo de Saque] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_SAQUE_AREA_USUARIO, "Botão Voltar (tela de Saque na Área do Usuário)")
        time.sleep(2)

        # PASSO 114: Clicar em um botão [Clicar em Pedidos de saques] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_PEDIDOS_DE_SAQUES, "Link/Botão Pedidos de saques")
        time.sleep(2)
        # PASSO 115: Verificar se um elemento é exibido [Elemento Tipo de transação] 
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ELEMENTO_TIPO_TRANSACAO, "Elemento Tipo de transação (Pedidos de Saques)")
        # PASSO 116: Clicar em um botão [Seta de voltar no topo de Pedidos de saques] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_PEDIDOS_DE_SAQUES, "Botão Voltar (tela de Pedidos de Saques)")
        time.sleep(2)

        # PASSO 117: Clicar em um botão [Clicar em Histórico de depósitos] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_HISTORICO_DE_DEPOSITOS, "Link/Botão Histórico de depósitos")
        time.sleep(2)
        # PASSO 118: Verificar se um elemento é exibido [Elemento Data/Hora] 
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ELEMENTO_DATA_HORA_HISTORICO_DEPOSITOS, "Elemento Data/Hora (Histórico de Depósitos)") 
        time.sleep(2)
        # PASSO 119: Clicar em um botão [Seta de voltar no topo de Histórico de depósitos] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_HISTORICO_DE_DEPOSITOS, "Botão Voltar (tela de Histórico de Depósitos)")
        time.sleep(2)

        # PASSO 120: Clicar em um botão [Clicar em Transações de cassino] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_TRANSACOES_DE_CASSINO, "Link/Botão Transações de cassino")
        time.sleep(2)
        # PASSO 121: Verificar se um elemento é exibido [Elemento Bônus ID da aposta] 
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ELEMENTO_BONUS_ID_APOSTA, "Elemento Bônus ID da aposta (Transações de Cassino)")
        # PASSO 122: Clicar em um botão [Seta de voltar no topo de Transações de cassino] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_VOLTAR_TOPO_TRANSACOES_DE_CASSINO, "Botão Voltar (tela de Transações de cassino)")
        time.sleep(2)

        # PASSO 123: Clicar em um botão [Clicar em Sair] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_SAIR, "Link/Botão Sair")
        time.sleep(2)
        # PASSO 124: Verificar se um elemento é exibido [Elemento Lembrete] 
        verificar_elemento_exibido_com_log(driver, By.XPATH, XPATH_ELEMENTO_LEMBRETE_SAIR, "Elemento Lembrete (Modal de Saída)")
        # PASSO 125: Clicar em um botão [Clicar em fechar modal] 
        aguardar_e_clicar_com_log(driver, By.XPATH, XPATH_BOTAO_CONFIRMAR_SAIDA, "Botão Fechar Modal (Lembrete de Saída)")
        time.sleep(2)


        print("\n--- FLUXO DE TESTE PRINCIPAL CONCLUÍDO ---")
        print("Verifique o console e o arquivo de log para resultados detalhados.")

    except Exception as e_critico:
        log_error("ERRO CRÍTICO NÃO TRATADO NO FLUXO PRINCIPAL DO TESTE", "N/A - Erro Geral", e_critico)
        try:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            nome_arquivo_screenshot = f"erro_critico_screenshot_{timestr}.png"
            driver.save_screenshot(nome_arquivo_screenshot)
            log_error("Screenshot de erro crítico salvo", nome_arquivo_screenshot, "")
        except Exception as ss_error:
            log_error("Falha ao salvar screenshot de erro crítico", "", ss_error)
    finally:
        print("\nAguardando alguns segundos antes de fechar o navegador...")
        time.sleep(5) 
        if 'driver' in locals() and driver: # Garante que driver existe
            driver.quit()
            print("WebDriver fechado.")
        finalizar_log()

if __name__ == "__main__":
    executar_teste()
