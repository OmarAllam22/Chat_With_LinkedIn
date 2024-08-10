from selenium import webdriver

class AskLogIn:
    def __init__(self, chrome_driver_path):
        self.driver = webdriver.Chrome(chrome_driver_path) 
        self.driver.get("https://linkedin.com/uas/login")
        while(True):
            if (self.driver.current_url == "https://www.linkedin.com/feed/"):
                break
        print("✔✔✔LogIn Succeeded✔✔✔")

    def get_driver(self):
        return self.driver

