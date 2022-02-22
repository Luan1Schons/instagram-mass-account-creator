# coding=utf-8
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from colorama import Fore
from seleniumwire import webdriver
from time import sleep
from fake_useragent import UserAgent
from confs.proxy import PROXY_INFO
from confs.debug import DEBUG
import accountInfoGenerator as account
import argparse
import requests
import os
import createExtensionChrome as ChromeExtension

# Security
if(DEBUG.DEBUG == False):
        sleep(60)

while True:

        # Config Proxy
        options_proxy = {
                'proxy': {
                        'http': PROXY_INFO.HTTP,
                        'https': PROXY_INFO.HTTPS,
                        'no_proxy': PROXY_INFO.NO_PROXY
                }
        }

        # running the browser
        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--firefox", action="store_true", help="Use Firefox - geckodriver")
        group.add_argument("--chrome", action="store_true", help="Use Firefox - geckodriver")

        args = parser.parse_args()
        ua = UserAgent()
        userAgent = ua.random

        # for firefox driver : 
        if args.firefox:
                options = FirefoxOptions()
                options.headless = DEBUG.DEBUG_FIREFOX_HEADLESS
                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", userAgent)
                driver = webdriver.Firefox(executable_path=r"./geckodriver.exe", seleniumwire_options=options_proxy, options=options)

        # for firefox driver :
        if args.chrome:

                """" CREATE EXTENSION ON GOOGLE CHROME ENVIRONMENT """""

                try:
                        ChromeExtension.create_proxy_extension(PROXY_INFO.PROXY_EXTENSION)
                except Exception as e:
                        print(e)
                        exit()

                executable_path = "./chromedriver.exe"
                os.environ["webdriver.chrome.driver"] = executable_path
                options = ChromeOptions()
                options.headless = DEBUG.DEBUG_CHROME_HEADLESS
                options.add_argument(f'user-agent={userAgent}')
                options.addArguments("--disable-gpu");
                options.addArguments("--disable-dev-shm-usage");
                options.addArguments("--no-sandbox");
                options.add_extension('./assets/chrome_extensions/proxy_auth.zip')
                driver = webdriver.Chrome(executable_path=r"./chromedriver.exe", seleniumwire_options=options_proxy, options=options)

        # DEBUG get proxy use confirmation
        if(DEBUG.DEBUG == True):
                driver.get('https://www.whatismyip.org/my-ip-address')
                sleep(1)

                # accepting cookies window
                try:
                        cookieWhatsMyIp = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/button[2]').click()
                except Exception as e: pass

                try:
                        ip = driver.find_element_by_xpath('//html/body/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/span')
                        city = driver.find_element_by_xpath('//html/body/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/span')
                        region = driver.find_element_by_xpath('//html/body/div[2]/div/div[2]/table/tbody/tr[3]/td[2]/span')
                        country = driver.find_element_by_xpath('//html/body/div[2]/div/div[2]/table/tbody/tr[4]/td[2]/span')

                        print("========================================================")
                        print("Informações de Rede (Proxy):")
                        print("\nIP:" + ip.text + "\nCidade:" + city.text + "\nRegião:" + region.text + "\nPaís:"+country.text)
                        print("========================================================")
                except Exception as e: print(e)

        print(Fore.YELLOW + "Iniciando criação de contas em massa...")

        ## Instagram
        sleep(1)
        driver.get('https://instagram.com/accounts/emailsignup')
         # importing the box information

        box_url = 'https://10minutesemail.net/getInbox'
        address_url = 'https://10minutesemail.net/getEmailAddress'
        main_page = 'https://10minutesemail.net'

        # main request
        main_page_req = requests.post(main_page)

        address_request = requests.post(address_url,cookies=main_page_req.cookies)

        address_data = address_request.json()

        # the email address string
        mail_address = str(address_data['address'])

        # recovery code string
        reco_key = str(address_data['recover_key'])

        print("Chave para recuperar email:" + reco_key)

        # accepting cookies window
        try:
                cookie = driver.find_element_by_xpath('/html/body/div[4]/div/div/button[1]').click()
        except Exception as e:
                print(Fore.GREEN + "Não houve necessidade de clickar para aceitar o cookie.")

        sleep(5)
        name = account.username()
        completeName = account.generatingName()
        # fill email
        email_field = driver.find_element_by_name('emailOrPhone')
        fake_email = mail_address
        email_field.send_keys(fake_email)
        # fill full
        fullname_field = driver.find_element_by_name('fullName')
        fullname_field.send_keys(completeName)
        #fill username
        username_field = driver.find_element_by_name('username')
        username_field.send_keys(name)

        # Fill password value

        passwd = account.generatePassword()
        password_field = driver.find_element_by_name('password')
        password_field.send_keys(passwd)  # You can determine another password here.

        sleep(1)
        try:
                driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div[7]/div/button[1]").click()
        except: exit()

        unavail_mess = "Esse nome de usuário não está disponível. Tente outro nome."
        sleep(1)
        # generating a new username if unavailable

        try :
                unavailable_user = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div[8]/p').text
                if unavailable_user == unavail_mess :
                        print(Fore.LIGHTWHITE_EX + 'Gerando novo usuário..')
                        username_clear = driver.find_element_by_name('username').clear()
                        sleep(1)
                        username_field.send_keys(name,Keys.ENTER)

        except Exception as e:
                pass

        sleep(1)

        #submit form
        try:
                driver.find_element_by_xpath("/html/body/div[1]/section/main/div/div/div[1]/div/form/div[7]/div/button[1]").click()
        except Exception as e: pass

        # Preenche datas de aniversário com +18 (Aleatório)
        sleep(1)
        try:
                driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select").click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select/option[4]"))).click()

                driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select").click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select/option[10]"))).click()

                driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select").click()
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select/option[27]"))).click()

                WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[6]/button"))).click()
        except Exception as e:
                print(Fore.RED + "Não foi possível submeter ao formulário.")
                exit()

        sleep(1)

        #  getting the verification code
        # email box request

        box_req = requests.post(box_url, cookies=main_page_req.cookies).json()
        print(Fore.LIGHTWHITE_EX + 'Esperando o código..')
        while box_req == []:
                box_req = requests.post(box_url, cookies=main_page_req.cookies).json()
                sleep(10)
        else:
                dic_conv = box_req[0]
                code_mess = dic_conv['subject']
                code = code_mess[0:6]
                print(Fore.GREEN + 'Código :'+ code)

        # fill instagram security code  
        driver.find_element_by_name('email_confirmation_code').send_keys(code, Keys.ENTER)
        sleep(1)
        try:
                not_valid = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[4]/div')

                if not_valid.text == "That code isn't valid. You can request a new one.":
                
                        sleep(1)
                        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[1]/div[2]/div/button').click()
                        sleep(1)
                        confInput = driver.find_element_by_name('email_confirmation_code')
                        confInput.send_keys(Keys.CONTROL + "a")
                        confInput.send_keys(Keys.DELETE)
                        confInput.send_keys(code, Keys.ENTER)

        except Exception as e:
                print(e)

        sleep(10)
        try:
                error = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[4]/div')
                print(Fore.RED + "ERRO: " + error.text)
                exit()
        except Exception as e:
                print(e)

        print(Fore.LIGHTWHITE_EX + "========================================================")
        print(Fore.LIGHTWHITE_EX + "Informações do usuário:")
        print(Fore.LIGHTWHITE_EX + "========================================================")
        print(Fore.LIGHTWHITE_EX + 'Nome completo: ' + completeName)
        print(Fore.LIGHTWHITE_EX + 'Usuário: ' + name)
        print(Fore.LIGHTWHITE_EX + 'Email: ' + fake_email)
        print(Fore.LIGHTWHITE_EX + 'Senha gerada: ' + passwd)
        print(Fore.LIGHTWHITE_EX + "========================================================")

        filepath = "./accounts.txt"
        with open('accounts.txt', 'a') as file:
                file.write('\n')
                file.write("\n================================\n" + name + "\n" + passwd + "\n" + fake_email)

        print(Fore.GREEN + "Conta de usuário criada com sucesso")

sleep(60)
driver.close()
