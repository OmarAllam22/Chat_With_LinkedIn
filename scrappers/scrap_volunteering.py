from bs4 import BeautifulSoup
import time

class ScrapVolunteering:
    def __init__(self, driver, profile_link, section_soup):
        self.driver = driver
        self.profile_link = profile_link
        self.soup = section_soup
        self.footer = self.soup.find("div",{"class":"pvs-list__footer-wrapper"})


    def _extract(self, section_soup, is_more):
        volunteering_list = [] 
        if is_more:
            items = [item for item in section_soup.find("section",{"class":"artdeco-card"}).find("ul").children if item.name=='li']
        else:
            items = [item for item in section_soup.find("ul").children if item.name=='li']
        for item in items:
            title = item.find("div", {"class":"mr1"}).find("span",{"class":"visually-hidden"}).get_text()
            organization = item.find("span", {"class":"t-14"}).find("span",{"class":"visually-hidden"}).get_text()
            volunteering_list.append(f"{title} at {organization}")
        return volunteering_list


    
    def get_output(self):
        """
        output here is list containing all the skills.
        """
        if self.footer != None:
            show_more_link = self.footer.find("a").get('href')
            self.driver.get(show_more_link)
            temp_full_page_src = self.driver.page_source
            temp_full_page_soup = BeautifulSoup(temp_full_page_src, "lxml")
            time.sleep(3)
            self.driver.get(self.profile_link+"#arrow-left-medium") # to return to the main page after entering the show-more-projects arrow.
            return self._extract(temp_full_page_soup, is_more=True)
        else:
            return self._extract(self.soup, is_more=False)
        