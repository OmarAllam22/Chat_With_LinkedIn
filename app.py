
import streamlit as st
import time
import webbrowser

from scrappers.ask_login import AskLogIn
from scrappers.full_profile_scrapper import ScrapLinkedInProfile
from resume_builder.resume_chat import ResumeChat
from linkedin_chatbot.linkedin_chat import LinkedInChat
from termcolor import colored

# Initializing chat objects

def scrap_and_intialize():
  login_object = AskLogIn(chrome_driver_path="chromedriver.exe",
                          profile_link=None)

  driver = login_object.get_driver()
  profile_link = login_object.get_profile_link()

  scrapper_object = ScrapLinkedInProfile(driver=driver, profile_link=profile_link)
  profile_dictionary = scrapper_object.scrap_all_sections()
  linkedin_chat_object = LinkedInChat(profile_dictionary)
  resume_chat_object = ResumeChat(linkedin_chat_object)
  return profile_link, profile_dictionary, linkedin_chat_object, resume_chat_object

def response_generator(chat_object, prompt):
    for chunk in chat_object.generate_response(prompt):
        yield chunk
        time.sleep(0.005)

def generate_resume_from_profile(profile_dictionary):
   profile_dictionary = st.session_state.res.update_linkedin_dict(profile_dictionary)
   profile_dictionary_as_html = st.session_state.res.get_sections_as_html(profile_dictionary)
   resume_html_dict = eval(profile_dictionary_as_html.strip("```json").strip("\n```"))

   with open("resume_builder/pre_template.html", "r", encoding='utf-8') as f:
      content = f.read()

   filled_html = content.format(name=resume_html_dict['person_name'],
                              headline=resume_html_dict['person_headline'],
                              profile_link= st.session_state.profile_link,
                              summary=resume_html_dict['about'],
                              education= resume_html_dict['education'],
                              experience= resume_html_dict['experience'],
                              projects= resume_html_dict['projects'],
                              skills= resume_html_dict['skills'],
                              courses=resume_html_dict["licenses_and_certifications"]
                              )

   file_path = r"resume_builder\template.html"
   with open(file_path, "w", encoding='utf-8') as f:
      f.write(filled_html)
   return file_path

if "scrap_and_initialize" not in st.session_state:
   with st.spinner('Wait until we scrap your LinkedIn profile...'):
      profile_link, profile_dictionary, linkedin_chat_object, resume_chat_object = scrap_and_intialize()
      st.session_state.profile_link = profile_link
      st.session_state.profile = profile_dictionary
      st.session_state.lnkdin = linkedin_chat_object
      st.session_state.res = resume_chat_object
      st.session_state.scrap_and_initialize = True
   st.success("Done with scrapping 😀")

if "messages" not in st.session_state:
   st.session_state.messages = []


st.title("Chat With LinkedIn")
#st.sidebar.markdown('<p style="font-size: 20px;">Choose a chat:</p>', unsafe_allow_html=True)
chat_option = st.sidebar.selectbox("Choose a chat type:", ["LinkedIn Chat 💦", "Resume Chat 🔻"])
#st.sidebar.markdown("<br></br>", unsafe_allow_html=True)

if chat_option == 'LinkedIn Chat 💦':
   chat_object = st.session_state.lnkdin
elif chat_option == 'Resume Chat 🔻':
   chat_object = st.session_state.res

for message in st.session_state.messages:
   with st.chat_message(message['role']):
      st.markdown(message['content']) 

if prompt:= st.chat_input("Type your message here 😊"):
   if (prompt== "update") and chat_object == st.session_state.lnkdin:
      st.session_state.profile = st.session_state.lnkdin.update_linkedin_dict(st.session_state.profile)
      st.success("Updating successfully")

   else:
      with st.chat_message("user"):
         st.markdown(prompt)
         st.session_state.messages.append({"role":"user",
                                       "content":prompt})

      with st.chat_message("assistant"):
         response = st.write_stream(response_generator(chat_object,prompt))
      
      st.session_state.messages.append({"role":"assistant",
                                       "content":response})

if st.sidebar.button("See current resume"):
   with st.sidebar.status("Generating resume..."):
      resume_path = generate_resume_from_profile(st.session_state.profile)
      webbrowser.open(resume_path, new=2)
   st.success("Resume generated ✔")
