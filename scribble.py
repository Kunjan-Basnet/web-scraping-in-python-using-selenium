from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from seleniumbase import SB
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

#driver=webdriver.Chrome()
with SB(uc=True,incognito=True,maximize=True,locale_code='en',skip_js_waits=True,headless=False) as sb:
    url='https://xyz.com/'
    sb.get(url)

    element=sb.find_element(By.XPATH,"//div[contains(@class,'hz')]//table[contains(@class,'hn')]")
   
    
    def scroll_to_view(sb,element):
        options={
            "behavior":"smooth",
            "block":"end",
            "inline":"end"
        }
        sb.execute_script("arguments[0].scrollIntoView(arguments[1]);",element,options)

    scroll_to_view(sb,element)

    time.sleep(2)
    

    order1=WebDriverWait(sb,15).until(
        EC.presence_of_all_elements_located((By.XPATH,"//td[contains(@class,'dx eb ek ex')]//a[contains(@class,'PartNbrLnk')]"))
    )
    
    for ord in order1: 
  
        ord.click()
        input_qnt=sb.wait_for_element("//input[contains(@class,'InLnOrdWebPartLayout_InpBx add-to-order-qty-inline')]",timeout=15)
        input_qnt.clear()
        input_qnt.send_keys("2")
        input_qnt.send_keys(Keys.RETURN)
        time.sleep(6)
        ord.click()
        



        
            
    ordbtn=sb.find_element(By.XPATH,".//a[contains(@class,'masthead-nav-anchor')]")
    ordbtn.click()
    time.sleep(4)
    sb.quit()
    