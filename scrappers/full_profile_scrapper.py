from bs4 import BeautifulSoup

from scrappers.scrap_personal_info import ScrapPersonalInfo
from scrappers.scrap_about import ScrapAbout
from scrappers.scrap_featured import ScrapFeatured
from scrappers.scrap_experience import ScrapExperience
from scrappers.scrap_education import ScrapEducation
from scrappers.scrap_certification import ScrapCertification
from scrappers.scrap_projects import ScrapProjects
from scrappers.scrap_skills import ScrapSkills
from scrappers.scrap_volunteering import ScrapVolunteering

class ScrapLinkedInProfile:
    def __init__(self, driver, profile_link):
        self.driver = driver
        self.profile_link = profile_link
        
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
        self.volunteering = "`Volunteering` section wasn't found."



    def scrap_all_sections(self):
        # scrap sections (about, experience, education ... etc)
        for section in self.profile_card_sections:
            section_name = section.find("div").get('id')
            # the following is because sometimes about = "" and and so on.
            section_names = ['about', 'featured', 'experience', 'education', 'licenses_and_certifications','projects','skills', "volunteering_experience"]
            if section is None:
               self.scrap_all_sections() 
            
            if section_name == section_names[0]:
                try:
                    self.about = self._getAbout()
                    print(f"{section_name} section scrapped successfully ✔")
                except:
                    self.about = f"{section_name} section wasn't found."
                    print(f"{section_name} ❌")
            elif section_name == section_names[1]:
                try:
                    self.featured = self._getFeatured(section)
                    print(f"{section_name} section scrapped successfully ✔")
                except:
                    self.featured = f"{section_name} section wasn't found."
                    print(f"{section_name} ❌")
            elif section_name == section_names[2]:
                try:
                    self.experience = self._getExperience(section)
                    print(f"{section_name} section scrapped successfully ✔")
                except:
                    self.experience = f"{section_name} section wasn't found."
                    print(f"{section_name} ❌")
            elif section_name == section_names[3]:
                try:
                    self.education = self._getEducation(section)
                    print(f"{section_name} section scrapped successfully ✔")
                except:
                    self.education =  f"{section_name} section wasn't found."
                    print(f"{section_name} ❌")
            elif section_name == section_names[4]:
                try:
                    self.certificate = self._getCertificate(section)
                    print(f"{section_name} section scrapped successfully ✔")
                except:
                    self.certificate = f"{section_name} section wasn't found."
                    print(f"{section_name} ❌")
            elif section_name == section_names[5]:
                try:
                    self.projects = self._getProjects(section)
                    print(f"{section_name} section scrapped successfully ✔")
                except:
                    self.projects = f"There is a internet connection problem scrapping {section_name}"
                    print(f"{section_name} ❌")
            elif section_name == section_names[6]:
                try:
                    self.skills = self._getSkills(section)
                    print(f"{section_name} section scrapped successfully ✔")
                except:
                    self.skills = f"{section_name} section wasn't found."
                    print(f"{section_name} ❌")
            elif section_name == section_names[7]:
                try:
                    self.self.volunteering = self._getVolunteering(section)
                    print(f"{section_name} section scrapped successfully ✔")
                except:
                    self.skills = f"{section_name} section wasn't found."
                    print(f"{section_name} ❌")

        # scrap personal info (name, headline)
        self.personal_info = self._getPersonalInfo()

        return {
            "name":self.personal_info['name'],
            "headline":self.personal_info['headline'],
            "about":self.about,
            "featured": self.featured,
            "experience":self.experience,
            "education":self.education,
            "licenses_and_certifications":self.certificate,
            "projects":self.projects,
            "skills":self.skills,
            "volunteering": self.volunteering
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
    
    def _getVolunteering(self, section_soup):
        object = ScrapVolunteering(self.driver, self.profile_link, section_soup)
        return object.get_output()