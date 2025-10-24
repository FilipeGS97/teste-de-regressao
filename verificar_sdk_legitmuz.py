# Houve um período que tivemos problemas na exibição do modal, no processo de registro de usuários. Esse problema acontecia 
# em momentos aleatórios do dia e afetava qualquer pessoa que tentasse se cadastrar no site. Logo, desenvolvi essa automação para 
# executar várias vezes ao longo do dia, utilizando um arquivo .bat para repetir o processo em determinado intervalo de tempo. 

# adicionei uma função que enviava notificação no telegram para alertar quando o problema ocorresse.

import asyncio
from telegram import Bot
import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Função para enviar a notificação via Telegram
async def send_notification(message):
    bot_token = '711891810:AAH_d_zFP_6PaRsrthetjr36IWyGddOU'  # Substitua pelo token do seu bot
    chat_id = '1596049146'  # Substitua pelo chat_id de quem deve receber a notificação
    bot = Bot(token=bot_token)

    try:
        # Enviar mensagem de notificação
        await bot.send_message(chat_id=chat_id, text=message)
        print("Notificação enviada com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar a notificação: {e}")

# Usando o Service com o WebDriver Manager (automático para buscar a versão do driver)
service = Service(ChromeDriverManager().install())

# Configurando o Chrome para rodar em modo headless (sem abrir o navegador)
#chrome_options = Options()
#chrome_options.add_argument("--headless")  # Ativa o modo headless
#chrome_options.add_argument("--disable-gpu")  # Desativa a aceleração de GPU (para evitar problemas no headless)
#chrome_options.add_argument("--no-sandbox")  # Desativa o sandbox (importante para rodar em alguns ambientes, como Docker)

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--ignore-certificate-errors")  # Adicione isso aqui
chrome_options.add_argument("--enable-logging")  # Ativa o logging
chrome_options.add_argument("--v=1")  # Configura o nível de log


# Inicializando o WebDriver (Chrome)
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # Acessar a URL especificada
    driver.get("https://x2bet.com/BR/register")

    cookie_xpath = "//*[@id='__nuxt']/main/div[5]/div/div/div[2]/button"  # Insira o XPath correto do campo CPF
    cookie_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, cookie_xpath)))
    cookie_button.click()

    # Preencher o campo CPF
    cpf_xpath = "//*[@id='document']"
    cpf_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, cpf_xpath)))
    cpf_input.send_keys("20698690400")  # Substitua pelo CPF desejado
    time.sleep(10)

    # Preencher o campo RG
    rg_xpath = "//*[@id='identity']"
    rg_input = driver.find_element(By.XPATH, rg_xpath)
    rg_input.send_keys("12345678")  # Substitua pelo RG desejado

    # Clicar no botão "Avançar"
    avancar_xpath = "//*[@id='__nuxt']/main/div[3]/div/div/div/div[2]/div/div/form/div[3]/button"
    try:
        avancar_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, avancar_xpath)))
        avancar_button.click()
    except Exception as e:
        print(f"Erro ao clicar no botão 'Avançar': {e}")
        # Enviar notificação se falhar
        asyncio.run(send_notification("Falha ao clicar no botão 'Avançar'"))

    # Aguardar 1 segundo
    time.sleep(3)

    # Verificar se o campo Email está visível
    email_xpath = "//*[@id='email']"
    try:
        email_input = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, email_xpath)))
        print("Campo Email encontrado.")

        # Preencher os campos restantes
        email_input.send_keys("josefelipe@gmail.com")
        telefone_xpath = "//*[@id='phone']"
        telefone_input = driver.find_element(By.XPATH, telefone_xpath)
        telefone_input.send_keys("83991835107")

        senha_xpath = "//*[@id='password']"
        senha_input = driver.find_element(By.XPATH, senha_xpath)
        senha_input.send_keys("@bet2024")

        confirmar_senha_xpath = "//*[@id='password_confirmation']"
        confirmar_senha_input = driver.find_element(By.XPATH, confirmar_senha_xpath)
        confirmar_senha_input.send_keys("@bet2024")

        cep_xpath = "//*[@id='zip']"
        cep_input = driver.find_element(By.XPATH, cep_xpath)
        cep_input.send_keys("58433135")

        # Esperar o campo Número da residência aparecer após preencher o CEP
        numero_residencia_xpath = "//*[@id='number']"
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, numero_residencia_xpath)))
        numero_residencia_input = driver.find_element(By.XPATH, numero_residencia_xpath)
        numero_residencia_input.send_keys("123")

        checkbox_xpath = "//*[@id='check']"
        checkbox = driver.find_element(By.XPATH, checkbox_xpath)
        checkbox.click()

        # Clicar no botão Criar conta
        criar_conta_xpath = "//*[@id='__nuxt']/main/div[3]/div/div/div/div[2]/div/div/form/div[3]/button[2]"
        criar_conta_button = driver.find_element(By.XPATH, criar_conta_xpath)
        criar_conta_button.click()

        # Aguardar 5 segundos
        time.sleep(5)

        # Verificar se o modal de sucesso foi exibido
        modal_xpath = "//*[@id='legitimuz-iframe']"
        try:
            modal = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, modal_xpath)))
            print("Cadastro bem-sucedido!")
        except:
            print("Cadastro mal-sucedido. Modal não encontrado.")
            # Enviar notificação se não encontrar o modal de sucesso
            asyncio.run(send_notification("Cadastro mal-sucedido. Modal não encontrado."))

    except Exception as e:
        print(f"Erro: {e}")
        asyncio.run(send_notification(f"Erro durante o processo: {e}"))

finally:
    
    data_e_hora = datetime.datetime.now()
    print(f"Data e hora: {data_e_hora.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Fechar o navegador após o script
    driver.quit()

