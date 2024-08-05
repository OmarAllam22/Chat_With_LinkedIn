from bs4 import BeautifulSoup

class ScrapFeatured:
    def __init__(self, driver, profile_link, section_soup):
        self.driver = driver
        self.profile_link = profile_link
        self.soup = section_soup


    def _extract(self, section_soup):
        posts = []
        items = [item for item in section_soup.find("ul").children if item.name=='li']
        check_tag = items[-1].find("a",{"aria-label":"Show all featured items"}) # this tag checks if there is more items or not
        if check_tag != None:
            link = check_tag.get("href")
            self.driver.get(link)
            temp_full_page_src = self.driver.page_source
            temp_full_page_soup = BeautifulSoup(temp_full_page_src, "lxml")
            self.driver.get(self.profile_link)
            items = [item for item in temp_full_page_soup.find("main").find("ul").children if item.name=='li']
        for item in items:
            try:
                post_content = item.find("a").find("span",{"dir":"ltr"}).get_text()
            except:
                try:
                    post_content = item.find("a").find("span",{"dir":"rtl"}).get_text()
                except:
                    continue
            posts.append(post_content)
        return posts


    
    def get_output(self):
        """
        output is a list of featured posts.
        """
        return self._extract(self.soup)