from bs4 import BeautifulSoup

class ScrapCertification:
    def __init__(self, driver, profile_link, section_soup):
        self.driver = driver
        self.profile_link = profile_link
        self.soup = section_soup

        self.footer = self.soup.find("div",{"class":"pvs-list__footer-wrapper"})

    def _extract_cert_and_institute(self, section_soup):
        cert_with_institute = {} 
        items = [item for item in section_soup.find("ul").children if item.name=='li']
        for item in items:
            cert_name = item.find("div",{"class":"justify-space-between"}).find("span",{"class":"visually-hidden"}).get_text()
            institute_name = item.find("div",{"class":"justify-space-between"}).find("span",{"class":"t-14"}).find("span",{"aria-hidden":"true"}).get_text()
            cert_with_institute[cert_name] = institute_name
        return cert_with_institute

    def _extract_more_cert_and_institute(self, full_page_soup):
        cert_with_institute = {} 
        items = [item for item in full_page_soup.find("section",{"class":"artdeco-card"}).find("ul").children if item.name=='li']
        for item in items:
            cert_name = item.find("div",{"class":"justify-space-between"}).find("span",{"class":"visually-hidden"}).get_text()
            institute_name = item.find("div",{"class":"justify-space-between"}).find("span",{"class":"t-14"}).find("span",{"aria-hidden":"true"}).get_text()
            cert_with_institute[cert_name] = institute_name
        return cert_with_institute
    
    def get_output_dictionary(self):
        if self.footer != None:
            show_more_link = self.footer.find("a").get('href')
            self.driver.get(show_more_link)
            temp_full_page_src = self.driver.page_source
            temp_full_page_soup = BeautifulSoup(temp_full_page_src, "lxml")
            self.driver.get(self.profile_link+"#arrow-left-medium") # to return to the main page after entering the show-more-projects arrow.
            return self._extract_more_cert_and_institute(temp_full_page_soup)
        else:
            return self._extract_cert_and_institute(self.soup)
        