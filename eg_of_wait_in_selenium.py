from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver=webdriver.Chrome()
driver.get('https://xyz.com/')

try:
    

    element2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Screws & Bolts"))
    )
    element2.click()

    element3 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Socket Head Screws"))
    )
    element3.click()

    element4 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Alloy Steel Socket Head Screws"))
    )
    element4.click()

    time.sleep(10)

    elem=driver.find_element(By.XPATH,"//td[contains(@class,'dx eb ek ex')]//a[contains(@class,'PartNbrLnk')]")
    print(elem.text)






finally:
    driver.quit()
