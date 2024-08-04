from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from scrap_experience import ScrapExperience

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
    

    def _collect_projects(self, section_soup):
        """
        helper function for the main `scrap_projects` function
        """
        projects_with_description = {}
        for child in section_soup.find("ul").children:
                if child.name == 'li':
                    project_name = (child.find("div",{"class":"mr1"})
                                        .find("span",{"class":"visually-hidden"})
                                        .get_text())
                    
                    project_description = (child.find("li",{"class":"pvs-list__item--with-top-padding"})
                                            .find("span",{"class":"visually-hidden"})
                                            .get_text())
                    
                    projects_with_description[project_name] = project_description
                else:
                    continue

        return projects_with_description


    def _collect_more_projects(self, section_soup):
        """
        helper function to `scrap_"more"_projects`
        """
        projects_with_description = {}
        projects_soup = section_soup.find("li",{"class":"artdeco-list__item"}).parent.findAll("li",{"class":"artdeco-list__item"})
        for child in projects_soup:
            if child.name == 'li':
                project_name = (child.find("div",{"class":"mr1"})
                                    .find("span",{"class":"visually-hidden"})
                                    .get_text())
                
                project_description = (child.find("li",{"class":"pvs-list__item--with-top-padding"})
                                        .find("span",{"class":"visually-hidden"})
                                        .get_text())
                projects_with_description[project_name] = project_description
            else:
                continue

        return projects_with_description


    def get_projects(self, section_soup):
        # check if there is "show more items" in this section or not
        footer = section_soup.find("div",{"class":"pvs-list__footer-wrapper"})
        
        if  footer != None:
                show_more_link = footer.find("a").get('href')
                self.driver.get(show_more_link)
                temp_section_src = self.driver.page_source
                temp_section_soup = BeautifulSoup(temp_section_src, "lxml")
                
                self.driver.get(self.profile_link+"#arrow-left-medium") # to return to the main page after entering the show-more-projects arrow.

                return self._collect_more_projects(temp_section_soup)
        else:
            return self._collect_projects(section_soup)


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
        return object.call_llm()
    

