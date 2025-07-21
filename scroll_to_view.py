from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from seleniumbase import SB
import time
from selenium.webdriver.common.action_chains import ActionChains

driver=webdriver.Chrome()
with SB(uc=True,incognito=True,maximize=True,locale_code="en",skip_js_waits=True,headless=False) as sb:
    url='https://xyz.com/'
    sb.driver.get(url)
   
    element=sb.driver.find_element(By.XPATH,".//div[contains(@class,'hz')]//table[contains(@class,'hn')]")
    
    def scroll_to_view(driver,element):
        options={
            "behavior":"smooth",
            "block":"end",
            "inline":"end"
        }
        driver.execute_script("arguments[0].scrollIntoView(arguments[1]);",element,options)

    scroll_to_view(sb.driver,element)    
    
    time.sleep(4)
    sb.driver.quit()


