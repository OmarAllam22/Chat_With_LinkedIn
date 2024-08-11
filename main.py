from ask_login import AskLogIn
from scrappers.full_profile_scrapper import ScrapLinkedInProfile
from resume_builder.resume_chat import ResumeChat
from linkedin_chatbot.linkedin_chat import LinkedInChat
from termcolor import colored

login_object = AskLogIn(chrome_driver_path="chromedriver.exe",
                        profile_link=None)

driver = login_object.get_driver()
profile_link = login_object.get_profile_link()

#-------------------------------------------------------------#

scrapper_object = ScrapLinkedInProfile(driver=driver, profile_link=profile_link)
profile_dictionary = scrapper_object.scrap_all_sections()

linkedin_chat_object = LinkedInChat(profile_dictionary)
resume_chat_object = ResumeChat(linkedin_chat_object)

while (True):
    inp = input("Omar22@linkedin_chat: ")
    if inp == "exit":
        profile_dictionary = linkedin_chat_object.update_linkedin_dict(profile_dictionary)
        break
    output_stream = linkedin_chat_object.generate_response(inp)
    for chunk in output_stream:
        print(colored(chunk.content, 'blue'), end="") 
while(True):
    inp = input("Omar22@resume_chat: ")
    if inp == "exit":
        profile_dictionary = resume_chat_object.update_linkedin_dict(profile_dictionary)
        break
    output_stream = resume_chat_object.generate_response(inp)
    for chunk in output_stream:
        print(colored(chunk.content, 'red'), end="")
print(profile_dictionary)
