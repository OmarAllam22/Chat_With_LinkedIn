class ScrapPersonalInfo:
    def __init__(self, soup):
        self.soup = soup

    def _getName(self):
        return self.soup.find("div",{"class":"mt2"}).find("h1").get_text()

    def _getHeadline(self):
        return self.soup.find("div",{"class":"mt2"}).find("div",{"class":"text-body-medium"}).get_text().strip()
        
    

    def get_output(self):
        return {"name": self._getName(),
                "headline": self._getHeadline()
                }