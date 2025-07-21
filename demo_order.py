from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from seleniumbase import SB
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

driver=webdriver.Chrome()
with SB(uc=True,incognito=True,maximize=True,locale_code='en',skip_js_waits=True,headless=False) as sb:
    url='https://xyz.com/'
    sb.driver.get(url)

    element=sb.driver.find_element(By.XPATH,"//div[contains(@class,'hz')]//table[contains(@class,'hn')]")
    
    def scroll_to_view(driver,element):
        options={
            "behavior":"smooth",
            "block":"end",
            "inline":"end"
        }
        driver.execute_script("arguments[0].scrollIntoView(arguments[1]);",element,options)

    scroll_to_view(sb.driver,element)

    time.sleep(2)
    

    order1=WebDriverWait(sb.driver,15).until(
        EC.presence_of_all_elements_located((By.XPATH,"//td[contains(@class,'dx eb ek ex')]//a[contains(@class,'PartNbrLnk')]"))
    )
    
    for ord in order1:    
        ord.click()
        input_qnt=WebDriverWait(sb.driver,15).until(
            EC.presence_of_element_located((By.XPATH,"//div[contains(@class,'InLnOrdWebPartLayout_QtyInp')]//input[contains(@class,'InLnOrdWebPartLayout_InpBx add-to-order-qty-inline')]"))
        )
        input_qnt.clear()
        input_qnt.send_keys("2")
        input_qnt.send_keys(Keys.RETURN)
        time.sleep(6)
        ord.click()
        
        
            
    ordbtn=sb.driver.find_element(By.XPATH,".//a[contains(@class,'masthead-nav-anchor')]")
    ordbtn.click()

    view_ord=WebDriverWait(sb.driver,10).until(
        EC.presence_of_all_elements_located((By.XPATH,"//div[contains(@class,'lines')]//div[contains(@class,'order-pad-line')]"))
    )

    product_name=[]
    product_description=[]
    product_number=[]
    product_quantity=[]
    product_per_price=[]
    product_total_price=[]

    for view in view_ord:
        product_name.append(view.find_element(By.XPATH,".//div[contains(@class,'title-text')]").text)
        product_description.append(view.find_element(By.XPATH,".//div[contains(@class,'details-web--view')]").text)
        product_number.append(view.find_element(By.XPATH,".//input[contains(@class,'line-part-number-input')]").get_attribute("value"))
        product_quantity.append(view.find_element(By.XPATH,".//input[contains(@class,'line-quantity-input')]").get_attribute("value"))
        product_per_price.append(view.find_element(By.XPATH,".//div[contains(@class,'line-section line-unit-price')]//div[1]").text)
        product_total_price.append(view.find_element(By.XPATH,".//div[contains(@class,'line-section line-total-price')]").text)


    dict={
        "Product-ID":product_number,
        "Product-Name":product_name,
        "Product-Description":product_description,
        "Product-Quantity(no. of packs)":product_quantity,
        "Price-Per-Pack":product_per_price,
        "Total-Amount":product_total_price
    }  

    df=pd.DataFrame(dict)
    print(df)

    df.to_csv("screws.csv")



    
    time.sleep(5)
    sb.driver.quit()    
            
            
  

   
    



