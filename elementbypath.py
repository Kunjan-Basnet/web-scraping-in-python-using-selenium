from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from seleniumbase import SB
import pandas as pd


driver=webdriver.Chrome()
with SB(uc=True,incognito=True,maximize=True,locale_code='en',skip_js_waits=True,headless=False) as sb:
    url='https://xyz.com/'
    sb.driver.get(url)
    time.sleep(10)

    elem1=sb.driver.find_elements(By.XPATH,".//td[contains(@class,'dx ea ek et')]")
    elem =sb.driver.find_elements(By.XPATH, ".//td[contains(@class, 'dx eb ek ex')]//a[contains(@class, 'PartNbrLnk')]")
    elem2=sb.driver.find_elements(By.XPATH,".//td[contains(@class,'dx ec ek fb fc')]")

    prt_qty=[]
    prt_nbr=[] 
    prt_pri=[]

    print("part quantity")

    for x in elem1:
      prt_qty.append(x.text)
      #print(x.text)

    print("part number")  

    for y in elem: 
      prt_nbr.append(y.text) 
      #print(y.text) 

    print("part price")  

    for z in elem2:
      prt_pri.append(z.text)
      #print(z.text)



    # prt_qty.append(elem1)
    # prt_nbr.append(elem)
    # prt_pri.append(elem2)

    dict={
       "part_number":prt_nbr,
       "part_quantity":prt_qty,
       "part_price":prt_pri
    }


    df=pd.DataFrame(dict)
    print(df)

    df.to_csv("parts.csv")

   # print(dict)




driver.quit()