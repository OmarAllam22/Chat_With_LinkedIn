from bs4 import BeautifulSoup

from scrappers.scrap_personal_info import ScrapPersonalInfo
from scrappers.scrap_about import ScrapAbout
from scrappers.scrap_featured import ScrapFeatured
from scrappers.scrap_experience import ScrapExperience
from scrappers.scrap_education import ScrapEducation
from scrappers.scrap_certification import ScrapCertification
from scrappers.scrap_projects import ScrapProjects
from scrappers.scrap_skills import ScrapSkills

class ScrapLinkedInProfile:
    def __init__(self, driver, profile_link):
        self.driver = driver
        self.profile_link = profile_link
        self.driver.get(self.profile_link)
        self.src = self.driver.page_source
        self.soup = BeautifulSoup(self.src, "lxml")
        self.profile_card_sections = self.soup.findAll("section",{"class":"pv-profile-card"}) # this returns a list of section codes
        self.personal_info = ""
        self.about = "`About` section wasn't found."
        self.featured = "`Featured` section wasn't found."
        self.experience =  "`Experience`section wasn't found."
        self.education =  "`Education` section wasn't found."
        self.certificate = "`Licenses_and_Certifications` section wasn't found."
        self.projects = "`Projects` section wasn't found."
        self.skills = "`Skills` section wasn't found."

    
    def scrap_all_sections(self):
        # scrap personal info (name, headline)
        self.personal_info = self._getPersonalInfo()
        # scrap sections (about, experience, education ... etc)
        for section in self.profile_card_sections:
            # the following is because sometimes about = "" and and so on.
            if section is None:
               self.scrap_all_sections() 
            section_name = section.find("div").get('id')
            if section_name == 'about':
                try:
                    self.about = self._getAbout()
                except:
                    self.about = "`About` section wasn't found."
            elif section_name == 'featured':
                try:
                    self.featured = self._getFeatured(section)
                except:
                    self.featured = "`Featured` section wasn't found."
            elif section_name == 'experience':
                try:
                    self.experience = self._getExperience(section)
                except:
                    self.experience =  "`Experience`section wasn't found."
            elif section_name == 'education':
                try:
                    self.education = self._getEducation(section)
                except:
                    self.education =  "`Education` section wasn't found."
            elif section_name == 'licenses_and_certifications':
                try:
                    self.certificate = self._getCertificate(section)
                except:
                    self.certificate = "`Licenses_and_Certifications` section wasn't found."
            elif section_name == 'projects':
                try:
                    self.projects = self._getProjects(section)
                except:
                    self.projects = "`Projects` section wasn't found."
            elif section_name == 'skills':
                try:
                    self.skills = self._getSkills(section)
                except:
                    self.skills = "`Skills` section wasn't found."

        return {
            "name":self.personal_info['name'],
            "headline":self.personal_info['headline'],
            "about":self.about,
            "featured": self.featured,
            "experience":self.experience,
            "education":self.education,
            "licenses_and_certifications":self.certificate,
            "projects":self.projects,
            "self.skills":self.skills
        }


    def _getPersonalInfo(self):
        object = ScrapPersonalInfo(self.soup)
        return object.get_output()

    def _getAbout(self):
        object = ScrapAbout(self.soup)
        return object.get_output() 
    
    def _getFeatured(self, section_soup):
        object = ScrapFeatured(self.driver, self.profile_link, section_soup)
        return object.get_output()
    
    def _getExperience(self, section_soup):
        object = ScrapExperience(section_soup)
        return object.get_output()

    def _getEducation(self, section_soup):
        object = ScrapEducation(section_soup)
        return object.get_output()

    def _getCertificate(self, section_soup):
        object = ScrapCertification(self.driver, self.profile_link, section_soup)
        return object.get_output()

    def _getProjects(self, section_soup):
        object = ScrapProjects(self.driver, self.profile_link, section_soup)
        return object.get_output()
    
    def _getSkills(self, section_soup):
        object = ScrapSkills(self.driver, self.profile_link, section_soup)
        return object.get_output()
    