#from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from time import sleep
from fake_useragent import UserAgent
import argparse
from seleniumwire import webdriver
import requests

def check():

    # ---------------------------------------------------------------
    # running the browser

    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--firefox", action="store_true", help="Use Firefox - geckodriver")
    group.add_argument("--chrome", action="store_true", help="Use Chrome - chromedriver")

    args = parser.parse_args()
    ua = UserAgent()
    userAgent = ua.random

    if args.firefox:
        options = {
            'proxy': {
                'http': 'http://veucdigital:123321_country-br_city-riodejaneiro@proxy.iproyal.com:12323',
                'https': 'http://veucdigital:123321_country-br_city-riodejaneiro@proxy.iproyal.com:12323',
                'no_proxy': 'dev_server:8080'
            }
        }
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", userAgent)
        driver = webdriver.Firefox(firefox_profile=profile, executable_path=r"./geckodriver.exe", seleniumwire_options=options)

    # for chrome driver :

    # for chrome driver :

    if args.chrome:
        from selenium.webdriver.chrome.options import Options

        options = Options()
        # proxy server definition
        # proxy parameter to options
        # options.add_argument('--proxy-server="%s"' % proxyUrl)
        options.add_argument(f'user-agent={userAgent}')
        driver = webdriver.Chrome(executable_path='./chromedriver.exe', options=options,
                                  desired_capabilities=capabilities)
    driver.get('http://www.whatsmyip.org/')
    # importing the box information
check()