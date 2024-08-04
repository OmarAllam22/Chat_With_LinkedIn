import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

class ScrapEducation:
    def __init__(self, section_soup):
        self.soup = section_soup

        self.prompt = (
            ChatPromptTemplate.from_messages(
                [
                    (
                    "system",
                        """
                        You will be given a text scrapped from LinkedIn Profile page sepcially the education section.
                        the text is given to you in the 'text' variable.
                        your task is to output a json with the following keys 'School',
                        'Duration_of_study', and 'Details_about_study' in the value of this key determine if it is still student or graduated. 
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
        1. takes the bs4 object of the education section (not the whole page bs4 object)
        2. loops through the education section items
        3. returns a list of json objecsts formatted like:
            ex: [{"School": "Mansoura University", "Duration_of_study": '2020-2025' ...},
                 {"School": "STEM School", "Duration_of_study": '2017-2020' ...}]
        """
        self.education_list = []
        self.education_items = [item for item in self.soup.find("ul").children if item.name == 'li']
        
        for item in self.education_items:
            text = item.get_text().replace("\n"," ").strip()
            result = self.chain.invoke({'text':text}).content.strip("```json\n").strip("\n```")
            try:
                result = eval(result)
            except:
                pass
            self.education_list.append(result)
        
        return self.education_list

