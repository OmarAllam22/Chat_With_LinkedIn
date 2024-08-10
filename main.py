<<<<<<< HEAD
from ask_login import AskLogIn
from scrappers.full_profile_scrapper import ScrapLinkedInProfile
from linkedin_chatbot.chat import LinkedInChat
from termcolor import colored

login_object = AskLogIn(chrome_driver_path="chromedriver.exe")

driver = login_object.get_driver()

profile_link = "https://www.linkedin.com/in/mostafa-edrees11/"

scrapper_object = ScrapLinkedInProfile(driver=driver, profile_link=profile_link)
profile_dictionary = scrapper_object.scrap_all_sections()

chat_object = LinkedInChat(profile_dictionary)
while (True):
    inp = input()
    if inp == "exit":
        break
    output_stream = chat_object.generate_response(inp)
    for chunk in output_stream:
        print(colored(chunk.content, 'blue'), end="") 
||||||| empty tree
=======
from ask_login import AskLogIn
from scrappers.full_profile_scrapper import ScrapLinkedInProfile

login_object = AskLogIn(chrome_driver_path="F:\My installed programs\web_drivers\chromedriver-win64\chromedriver.exe")

driver = login_object.get_driver()

profile_link = "https://www.linkedin.com/in/mostafa-edrees11/"

scrapper_object = ScrapLinkedInProfile(driver=driver, profile_link=profile_link)

profile_dictionary = scrapper_object.scrap_all_sections()
print(profile_dictionary)
>>>>>>> 0975ef95975ce9668ac6bef0070dadb9ac8120f8
