from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from scrap_experience import ScrapExperience
from scrap_education import ScrapEducation
from scrap_certification import ScrapCertification
from scrap_projects import ScrapProjects

class ScrapLinkedInProfile:
    def __init__(self, driver, profile_link):
        self.driver = driver
        self.profile_link = profile_link
        # Signing in LinkedIn
        self.driver.get("https://linkedin.com/uas/login")
        time.sleep(5)
        username = self.driver.find_element(By.ID, "username")
        username.send_keys("omarallam@std.mans.edu.eg")
        password = self.driver.find_element(By.ID, "password")
        password.send_keys("awzu_900")
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        # landing on profile
        self.driver.get(self.profile_link)
        
        # wrapping the html content in a bs4 soup
        self.src = self.driver.page_source
        self.soup = BeautifulSoup(self.src, "html.parser")

        # getting the sections inside the person profile
        self.profile_card_sections = self.soup.findAll("section",{"class":"pv-profile-card"}) # this returns a list of section codes

    
    def get_name(self):
        """
        scrap the person name in the profile.
        """
        self.name = (
            self.soup.find("div",{"class":"mt2"})
            .find("h1")
            .get_text()
            )
        return self.name

    def get_description(self):
        """
        scrap the description of the person in the profile.
        """
        self.description = (
            self.soup.find("div",{"class":"mt2"})
            .find("div",{"class":"text-body-medium"})
            .get_text().strip()
            )
        return self.description
    


    def get_about(self):
        """
        scrap the about section of the person in the profile.
        """
        self.about = (
            self.soup.find("div",{"class":"pv3"})
            .find("span",{"class":"visually-hidden"})
            .get_text()
            )
        return self.about
    

    def get_experience(self, section_soup):
        object = ScrapExperience(section_soup)
        return object.get_output_dictionary()
    

    def get_education(self, section_soup):
        object = ScrapEducation(section_soup)
        return object.get_output_dictionary()


    def get_certificate(self, section_soup):
        object = ScrapCertification(self.driver, self.profile_link, section_soup)
        return object.get_output_dictionary()


    def get_projects(self, section_soup):
        object = ScrapProjects(self.driver, self.profile_link, section_soup)
        return object.get_output_dictionary()