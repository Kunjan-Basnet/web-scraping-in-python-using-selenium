from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time

driver=webdriver.Chrome()
driver.get("http://www.python.org")
clickact=driver.find_element(By.ID,"about")
action=ActionChains(driver)
action.click(clickact)
action.perform()
time.sleep(6)
driver.quit()
