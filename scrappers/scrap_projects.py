from bs4 import BeautifulSoup
import time

class ScrapProjects:
    def __init__(self, driver, profile_link, section_soup):
        self.driver = driver
        self.profile_link = profile_link
        self.soup = section_soup

        self.footer = self.soup.find("div",{"class":"pvs-list__footer-wrapper"})
    

    def _extract(self, section_soup, is_more):
        projects_with_description = {}
        if is_more:
            projects_soup = section_soup.find("li",{"class":"artdeco-list__item"}).parent.findAll("li",{"class":"artdeco-list__item"})
        else:
            projects_soup = section_soup.find("ul").children
        for child in projects_soup:
            if child.name == 'li':
                project_name = (child.find("div",{"class":"mr1"})
                                    .find("span",{"class":"visually-hidden"})
                                    .get_text())    
                project_description = (child.find("li",{"class":"pvs-list__item--with-top-padding"})
                                        .find("span",{"class":"visually-hidden"})
                                        .get_text())
                projects_with_description[project_name] = project_description
        return projects_with_description


    def get_output(self):
        """
        output is a dictionary with keys as projects_names and values as projects_descriptions
        """
        if self.footer != None:
            show_more_link = self.footer.find("a").get('href')
            self.driver.get(show_more_link)
            temp_section_src = self.driver.page_source
            temp_section_soup = BeautifulSoup(temp_section_src, "lxml")
            time.sleep(3)
            self.driver.get(self.profile_link+"#arrow-left-medium") # to return to the main page after entering the show-more-projects arrow.
            return self._extract(temp_section_soup, is_more=True)
        else:
            return self._extract(self.soup, is_more=False)