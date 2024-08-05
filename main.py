from ask_login import AskLogIn
from scrappers.full_profile_scrapper import ScrapLinkedInProfile

login_object = AskLogIn(chrome_driver_path="F:\My installed programs\web_drivers\chromedriver-win64\chromedriver.exe")

driver = login_object.get_driver()

profile_link = "https://www.linkedin.com/in/mostafa-edrees11/"

scrapper_object = ScrapLinkedInProfile(driver=driver, profile_link=profile_link)

profile_dictionary = scrapper_object.scrap_all_sections()
print(profile_dictionary)
