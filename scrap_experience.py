import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

class ScrapExperience:
    def __init__(self, section_soup):
        self.soup = section_soup

        self.prompt = (
            ChatPromptTemplate.from_messages(
                [
                    (
                    "system",
                        """
                        You will be given a text scrapped from LinkedIn Profile page sepcially the experience section.
                        the text is given to you in the 'text' variable.
                        your task is to output a json with the following keys 'Company_name',
                        'Job_title' (or 'Job_titles' if a person serves more than once in this company).
                        values for 'Title' or 'Titles' include both the job title and details if exist about this title or titles.
                        possible subkeys for details may be (Employment_type (vallues for this may be: part-time, full-time, internship), Location, Description or Skills), 
                        Ignore any image files.
                        Output the dictionary only with out any other text,
                        """
                    ),
                    "human",
                        "{text}"
                ]
            )
        )

        os.environ["GOOGLE_API_KEY"] = "AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q"
        self.model = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

        self.chain = self.prompt | self.model

    def call_llm(self):
        """
        This function:
        1. takes the bs4 object of the experience section (not the whole page bs4 object)
        2. loops through the experience section items
        3. returns a list of json objecsts formatted like:
            ex: [{"Company_name": "CAT Reloaded", "job_title": "data scientist" ...},
                 {"Company_name": "IEEE", "job_title": "ML engineer" ...}]
        """
        self.experience_list = []
        self.experience_items = [item for item in self.soup.find("ul").children if item.name == 'li']
        
        for item in self.experience_items:
            text = item.get_text().replace("\n"," ").strip()
            result = self.chain.invoke({'text':text})
            self.experience_list.append(result)
        
        return self.experience_list

