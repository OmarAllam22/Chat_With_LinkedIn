from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
import random
import os

class ResumeChat:
    def __init__(self, linkedin_chat_object, start_from='chat'):
        
        self.config_num = str(random.randint(0,1000))

        self.messages_history = ChatMessageHistory()
        self.stored_messages = []
        
        self.linkedin_content = linkedin_chat_object.linkedin_content 

        if start_from == "chat":
            self.messages_history = linkedin_chat_object.messages_history # if there is no linkedIn chat, then chat_history will be empty and it will be filled with resume chat.

        elif start_from == "given_resume":
            """
            add here a document loader to get the text of the resume and 
            assign it to self.messages_history as ChatMessageHistory()
            """
            pass # -------------------------------------------------------------------------------------------------------<

        os.environ["GOOGLE_API_KEY"] = 'AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q'
        self.chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                Act as a seasoned recruiter crafting a standout resume. 
                Utilize the provided LinkedIn profile, chat history, and job description to create or enhance resume sections.
                If LinkedIn data is missing, generate compelling content aligned with the job description. 
                Prioritize clear, concise, and impactful language. 
                Focus on information relevant to the target job.
                Here is the LinkedIn profile content {linkedIn_profile}
                
                Your task is to help the person tailor his/her resume to his specified job description.
                
                Note: Be coincise and avoid lengthy messages with less information and always be specific to the person. 
                """),
                ("placeholder", "{chat_history}"),
                ("user", "{input}"),
            ]
        )

        self.chain = self.prompt | self.chat

        self.chain_with_message_history = RunnableWithMessageHistory(
            self.chain,
            lambda session_id: self.messages_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )


    def _summarize(self, chain_input):
        self.stored_messages = self.messages_history.messages
        if len(self.stored_messages) == 0:
            return False
        self.summarization_prompt = ChatPromptTemplate.from_messages(
            [
                ("placeholder", "{chat_history}"),
                (
                    "user",
                    """
                    Concisely summarize the conversation, focusing on key details related to LinkedIn profile analysis, job description integration, and resume content generation.
                    Highlight specific recommendations, challenges, or potential solutions discussed.  
                    """,
                ),
            ]
        )
        
        self.summarization_chain = self.summarization_prompt | self.chat
        
        self.summary_message = self.summarization_chain.invoke({"chat_history":self.stored_messages})
        self.messages_history.clear()
        self.messages_history.add_message(self.summary_message)
        
        return True
    
    def generate_response(self, user_input):
        self.chain_with_summarization = (
            RunnablePassthrough.assign(messages_summarized=self._summarize)
            | self.chain_with_message_history
        )

        self.chain_input = {"input": user_input, "linkedIn_profile": self.linkedin_content}
        self.output = self.chain_with_summarization.stream(self.chain_input,
                                             {"configurable": {"session_id": self.config_num}})
    
        return self.output 
    

    def update_linkedin_dict(self, old_linkedin_dict):
        self.update_linkedin_prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                    """
                    Act as a seasoned recruiter enhancing LinkedIn profile content. Given a profile as a JSON object and a chat history, 
                    refine existing profile sections based on recruiter best practices and conversation context. Prioritize clarity, conciseness, and impact, aligning content with the target job.

                    If a section's content is missing or marked as "`section_name_placeholder` wasn't found," generate appropriate content based on available information. 
                    Return the enhanced profile as a JSON dictionary the same keys given as input.

                    This is the messages history: {chat_history}.
                    """ 
                ),("human","{linkedIn_profile}")
            ]
        )

        self.updating_chain = self.update_linkedin_prompt | self.chat
        
        self.updated_linkedin_dictionary = self.updating_chain.invoke({"chat_history":self.stored_messages,
                                                           "linkedIn_profile":old_linkedin_dict}).content
        return self.updated_linkedin_dictionary
    

    def get_sections_as_html(self, updated_linkedin_dict):
        self.get_resume_as_html = ChatPromptTemplate.from_messages(
            [
                ("system",
                    """
                    You have solid grammer and formal writing skills and always think from recruiter's point of view.
                    Your task is to:
                    - take a json contains linkedIn profile content for a given person.
                    - return a json with the same keys but the values for each key (in ['about', 'experience', 'education', 'licenses_and_certifications','projects','skills']) is wrapped in html code according to the following:
                    * if the key was "about", its value is:
                    ```
                    <h2>Summary</h2><p>here is the about content</p>
                    ```
                    * if key was "experience", its value is:
                    ```
                    <h2>Experience</h2><ul><li><h4 style="display:inline">first position</h4><span style = "margin-right:30px; float:right;">duration from - to</span><h5>company of first position</h5><p>description about this position responsibilities (if not provided, generate summarized one)</p></li>"the other experience sections are put between <li></li> with the same format""No emojies are allowed"</ul> 
                    ```
                    * if key was "education", its value is:
                    ```
                    <h2>Education</h2><ul><li><h4>school name</h4><p>duration from - to</p><p> description if exist (may be the GPA or Grade. if not provided, leave it without any text)</p></li>"the other education sections are put between <li></li> with the same format"</ul>
                    ```
                    * if key was "licenses_and_certifications":
                    ```
                    <h2>Certifications</h2><ul><li> <h4>first certificate name</h4><p>certificate's organization</p></li>"the other certificates sections are put between <li></li> with the same format"</ul>
                    ```
                    * if key was "projects":
                    ```
                    <h2>Projects</h2><ul><li><h4>project name</h4><p>description of the project (if not provided, generate one with action verbs and good grammer that tailor the resume)</p></li>"the other projects are put here between <li></li> with the same format."</ul>

                    ```
                    if key was "skills":
                    ```
                    <h2>Skills</h2><ul><li>ARM</li>"the other skills sections are put between <li></li> with the same format"</ul>
                    ```
                    
                    If a section's content is missing or marked as "`section_name_placeholder` wasn't found," generate appropriate content based on available information. 
                    
                    Remember don't include general words in your answer (ex: Don't include [start date] - [end date] ... fill them with specific time instead or even make up them.)

                    Note: Return your answer as json dictionary with the keys ['person_name', 'person_headline', 'about', 'experience', 'education', 'licenses_and_certifications','projects','skills' ].

                    This is the messages history: {chat_history}.
                    """ 
                ),("human","{linkedIn_profile}")
            ]
        )

        self.html_chain = self.get_resume_as_html | self.chat
        
        self.output_html = self.html_chain.invoke({"chat_history":self.stored_messages,
                                                           "linkedIn_profile":updated_linkedin_dict}).content
        return self.output_html