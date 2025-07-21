from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver=webdriver.Chrome()
driver.get("http://www.python.org")
elem=driver.find_elements(By.CLASS_NAME,"container")
#file=open("hello.txt","w")
#file.write(elem.text)
for el in elem:
  print(el.text)
#file.close()
time.sleep(6)

#file=open("hello.txt","r")
#print(file.read())
driver.quit()