from bs4 import BeautifulSoup

class ScrapCertification:
    def __init__(self, driver, profile_link, section_soup):
        self.driver = driver
        self.profile_link = profile_link
        self.soup = section_soup
        self.footer = self.soup.find("div",{"class":"pvs-list__footer-wrapper"})


    def _extract(self, section_soup, is_more):
        cert_with_institute = {} 
        if is_more:
            items = [item for item in section_soup.find("section",{"class":"artdeco-card"}).find("ul").children if item.name=='li']
        else:
            items = [item for item in section_soup.find("ul").children if item.name=='li']
        for item in items:
            cert_name = item.find("div",{"class":"justify-space-between"}).find("span",{"class":"visually-hidden"}).get_text()
            institute_name = item.find("div",{"class":"justify-space-between"}).find("span",{"class":"t-14"}).find("span",{"aria-hidden":"true"}).get_text()
            cert_with_institute[cert_name] = institute_name
        return cert_with_institute

    
    def get_output(self):
        """
        output is a dictionary with keys as certificates_names and values as certificates_institutes.
        """
        if self.footer != None:
            show_more_link = self.footer.find("a").get('href')
            self.driver.get(show_more_link)
            temp_full_page_src = self.driver.page_source
            temp_full_page_soup = BeautifulSoup(temp_full_page_src, "lxml")
            self.driver.get(self.profile_link+"#arrow-left-medium") # to return to the main page after entering the show-more-projects arrow.
            return self._extract(temp_full_page_soup, is_more=True)
        else:
            return self._extract(self.soup, is_more=False)
        