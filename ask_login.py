from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

class AskLogIn:
    def __init__(self, chrome_driver_path, profile_link=None):

        self.profile_link = profile_link
        
        WINDOW_SIZE = "500,800"
        self.chrome_options = Options()
        #self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
        self.driver = webdriver.Chrome(executable_path=chrome_driver_path,
                                       chrome_options=self.chrome_options) 
        self.driver.get("https://linkedin.com/uas/login")
        while(True):
            if (self.driver.current_url == "https://www.linkedin.com/feed/"):
                break
        print("✔LogIn Succeeded✔")
        

        if self.profile_link:
            self.driver.get(self.profile_link)
        else:
            src = self.driver.page_source
            soup = BeautifulSoup(src, "lxml")
            while True:
                if self.profile_link:
                    break
                try:
                    self.profile_link = "https://www.linkedin.com" + soup.find("div",{"class":"scaffold-layout__sidebar"}).find("a").get('href')
                    self.driver.get(self.profile_link)
                except:
                    pass

    def get_driver(self):
        return self.driver
    
    def get_profile_link(self):
        return self.profile_link

