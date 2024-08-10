class ScrapAbout:
    def __init__(self, soup):
        self.soup = soup

    def get_output(self):
        return self.soup.find("div",{"class":"pv3"}).find("span",{"class":"visually-hidden"}).get_text()