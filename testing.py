from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import unittest

class google_search_test(unittest.TestCase):
    
    def setUp(self):
        
        print("setup") #every time a new test method is called, the setUp method is called freshly so as a result "setup" is printed twice when the program is runned.
        self.driver=webdriver.Chrome()
    
    def test_search_in_google(self):
        #self.driver.implicitly_wait(10)
        self.driver.get("https://www.google.com/")
        assert "Google" in self.driver.title
        self.elem=self.driver.find_element(By.NAME,"q")
        self.elem.send_keys("python")
        self.elem.send_keys(Keys.RETURN)

    def test_dummy(self):
        assert True
    
    def tearDown(self):
        self.driver.quit()

if __name__=="__main__":
    unittest.main()






