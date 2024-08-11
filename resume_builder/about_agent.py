from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
import os

class AboutAsHTML:
    def __init__(self, linkedin_chat_obj):

        self.linkedin_content = linkedin_chat_obj.linkedin_content
        self.linkedin_chat_history = linkedin_chat_obj.messages_history
        
        os.environ["GOOGLE_API_KEY"] = 'AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q'
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                You have solid grammer and formal writing skills and always think from recruiter's point of view.
                Your task is to help a person building his/her resume tailored to a specific job description given to (If the user asked to build the resume without specifing certain job description, ask him/her about it).
                You have access to chat history and a LinkedIn profile section's content.

                Your task is to output this json with the following two keys:
                 "section_name": the section name which user message about (it must be one of ["summary", "experience", "education", "projects","skills", "courses_and_certifications"] or `None` if the user asked a general irrelevant question.),
                  "section_content": the generated content put under the `section_name` (it is a description tailored to both the specific job description given by the user and the person's information related to this section). this content is taken after that and put in resume.
                
                Note: If user asked a general question, answer it from your knowledge. Always remember, you think as recruiter.                
                Remeber to be coincise in your response.
                Here is the LinkedIn profile content {linkedIn_profile} 
                """),
                ("placeholder", "{chat_history}"),
                ("user", "{input}"),
            ]
-------        )        
        self.chat = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                You have solid grammer and formal writing skills and always think from recruiter's point of view.
                You have access to a person's linkedIn content summary and chat history from a linkedin builder chat. 
                Your task is to 
                - write the `Summary` section in the resume that best matches this person and the specific job description.
                Return your answer in html format like this:
                ```
                <h3>Experience</h3><ul>
                <li>
                    <h4 style="display:inline">Position Title</h4>
                    <table>
                    <span style = "margin-right:30px; float:right;">duration (ex: Jan 2024 - Present)</span>
                    <h5>Company_name</h5>
                    <p>coincise and perfect description from the recruiter point of view</p>
                </li>  
                ```
                If more experiences exist put them inside <li></li> and so on.
                
                Take care:
                - Order experiences from recent to old.
                - not to repeat experiences and if the person repeat them in a messy way, organize them then return organized experience.
                - the content in chat history may make you edit what in the linkedin profile.
                
                Here is the linkedIn Profile content: {linkedin_profile}
                And here is the chat history: {chat_history}
                """)
            ]
        )

        self.chain = self.prompt | self.chat
    
    def getHTML(self):
        return self.chain.invoke({"linkedin_profile":self.linkedin_content,
                                  "chat_history":self.linkedin_chat_history}).content