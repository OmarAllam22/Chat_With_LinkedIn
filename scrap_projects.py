from bs4 import BeautifulSoup

class ScrapProjects:
    def __init__(self, driver, profile_link, section_soup):
        self.driver = driver
        self.profile_link = profile_link
        self.soup = section_soup

        self.footer = self.soup.find("div",{"class":"pvs-list__footer-wrapper"})
    

    def _extract_projects(self, section_soup):
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


    def _extract_more_projects(self, section_soup):
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


    def get_output_dictionary(self):
        if self.footer != None:
            show_more_link = self.footer.find("a").get('href')
            self.driver.get(show_more_link)
            temp_section_src = self.driver.page_source
            temp_section_soup = BeautifulSoup(temp_section_src, "lxml")
            self.driver.get(self.profile_link+"#arrow-left-medium") # to return to the main page after entering the show-more-projects arrow.
            return self._extract_more_projects(temp_section_soup)
        else:
            return self._extract_projects(self.soup)