from seleniumbase import SB
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from seleniumwire import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
proxy_url = f'http://brd-customer-hl_0595730b-zone-mcmaster_residential_proxies-country-us-city-chicago:nb47dn7759xo@brd.superproxy.io:33335'

seleniumwire_options = {
    'proxy': {
        'http': proxy_url,
        'https': proxy_url
    },
    'ca_certs': r'C:\Users\manik\Downloads\brightdata_proxy_ca'  # Path to your ca.crt file
}

options = Options()
# ... other options



with SB(proxy= proxy_url, wire=True, headless=True,) as sb:
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), seleniumwire_options=seleniumwire_options, options=options)
    previous_ip=None

    for x in range(8):

        driver.get("https://api.ipify.org/")
        #time.sleep(3)
        ip=driver.find_element(By.TAG_NAME,"pre")
        current_ip=ip.text
        tim=datetime.datetime.now()
        print(f"the {x+1} ip address is {ip.text} and current time is {tim}")
        if x==0:
            previous_ip=current_ip

        if current_ip==previous_ip:
            temp=tim

        else:
            time_interval=tim-temp
            print(f"the interval of two ips are {time_interval}")
            previous_ip=current_ip
            temp=tim


    driver.quit()
    
       

