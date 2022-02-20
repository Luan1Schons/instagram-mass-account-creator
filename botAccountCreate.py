from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import accountInfoGenerator as account
#from selenium import webdriver
from seleniumwire import webdriver
from selenium.webdriver import Firefox
from time import sleep
from fake_useragent import UserAgent
import argparse
import requests
import pathlib


while True:

        # Config Proxy
        options_proxy = {
                'proxy': {
                        'http': 'http://oxy123asdx:GbaTTyshca@4g.iproyal.com:4001',
                        'https': 'http://oxy123asdx:GbaTTyshca@4g.iproyal.com:4001',
                        'no_proxy': 'dev.local:8080'
                }
        }

        # ---------------------------------------------------------------
        # running the browser

        parser = argparse.ArgumentParser()
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--firefox", action="store_true", help="Use Firefox - geckodriver")

        args = parser.parse_args()
        ua = UserAgent()
        userAgent = ua.random

        # for firefox driver : 
        if args.firefox:
                options = Options()
                options.headless = False
                profile = webdriver.FirefoxProfile()
                profile.set_preference("general.useragent.override", userAgent)
                driver = webdriver.Firefox(executable_path=r"./geckodriver.exe", seleniumwire_options=options_proxy, options=options)


        driver.get('https://www.whatismyip.org/my-ip-address')
        sleep(2)
        # accepting cookies window
        try:
                cookieWhatsMyIp = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/button[2]').click()
        except Exception as e:
                print("Não foi possível aceitar os cookies.")

        sleep(3)
        try:
                ip = driver.find_element_by_xpath('//html/body/div[2]/div/div[2]/table/tbody/tr[1]/td[2]/span')
                city = driver.find_element_by_xpath('//html/body/div[2]/div/div[2]/table/tbody/tr[2]/td[2]/span')
                region = driver.find_element_by_xpath('//html/body/div[2]/div/div[2]/table/tbody/tr[3]/td[2]/span')
                country = driver.find_element_by_xpath('//html/body/div[2]/div/div[2]/table/tbody/tr[4]/td[2]/span')

                print("========================================================")
                print("Informações de Rede (Proxy):")
                print("\nIP:" + ip.text + "\nCidade:" + city.text + "\nRegião:" + region.text + "\nPaís:"+country.text)
                print("========================================================")
        except Exception as e:
                print(e)

        print("Iniciando criação de contas em massa...")
        sleep(2)
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
        print("========================================================")
        reco_key = str(address_data['recover_key'])
        print('Chave de recuperação: ' + reco_key)
        print("========================================================")

        sleep(2)
        # accepting cookies window
        try:
                cookie = driver.find_element_by_xpath('/html/body/div[4]/div/div/button[1]').click()
        except Exception as e:
                print(e)

        sleep(6)
        name = account.username()

        # fill email
        print("========================================================")
        email_field = driver.find_element_by_name('emailOrPhone')
        fake_email = mail_address
        email_field.send_keys(fake_email)
        print('Email: ' + fake_email)

        # fill full
        fullname_field = driver.find_element_by_name('fullName')
        fullname_field.send_keys(account.generatingName())
        print('Nome completo: '+ account.generatingName())
        #fill username
        username_field = driver.find_element_by_name('username')
        username_field.send_keys(name)
        print('Usuário: ' + name)

        # Fill password value

        passwd = account.generatePassword()
        password_field = driver.find_element_by_name('password')
        password_field.send_keys(passwd)  # You can determine another password here.

        print("Senha Preenchida: " + password_field.get_attribute('value'))
        print('Senha gerada: ' + passwd)
        sumbit = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/form/div[7]/div/button"))).click()
        print("========================================================")

        unavail_mess = "Esse nome de usuário não está disponível. Tente outro nome."
        sleep(1.2)
        # generating a new username if unavailable

        try :

                unavailable_user = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div/form/div[8]/p').text
                if unavailable_user == unavail_mess :
                        print('Gerando novo usuário..')
                        username_clear = driver.find_element_by_name('username').clear()
                        sleep(1)
                        username_field.send_keys(name,Keys.ENTER)

        except Exception as e:
                print(e)

        # Preenche datas de aniversário com +18 (Aleatório)
        sleep(1.2)
        driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select").click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[1]/select/option[4]"))).click()

        driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select").click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[2]/select/option[10]"))).click()

        driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select").click()
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[4]/div/div/span/span[3]/select/option[27]"))).click()

        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='react-root']/section/main/div/div/div[1]/div/div[6]/button"))).click()
        sleep(3)


        #  getting the verification code
        # email box request

        box_req = requests.post(box_url, cookies=main_page_req.cookies).json()
        print('Esperando o código..')
        while box_req == []:
                box_req = requests.post(box_url, cookies=main_page_req.cookies).json()
                sleep(10)
        else:
                dic_conv = box_req[0]
                code_mess = dic_conv['subject']
                code = code_mess[0:6]
                print('Código:'+ code)

        # fill instagram security code  
        driver.find_element_by_name('email_confirmation_code').send_keys(code, Keys.ENTER)
        sleep(15)
        try:

                not_valid = driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[2]/form/div/div[4]/div')
                if not_valid.text == 'O código não é valido.' :
                
                        sleep(1)
                        driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/div[1]/div[1]/div[2]/div/button').click()
                        sleep(5)
                        confInput = driver.find_element_by_name('email_confirmation_code')
                        confInput.send_keys(Keys.CONTROL + "a")
                        confInput.send_keys(Keys.DELETE)
                        confInput.send_keys(code, Keys.ENTER)

                        sleep(30)
                        print("Conta criada com sucesso.")

                        # get fileName from user
                        filepath = "./accounts.txt"

                        # Creates a new file
                        pathlib.Path(filepath).touch()
        except Exception as e:
                print(e)
                sleep(15)

        driver.close()
