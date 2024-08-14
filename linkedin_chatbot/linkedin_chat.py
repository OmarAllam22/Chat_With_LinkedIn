from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.runnables import RunnablePassthrough
import random
import os

class LinkedInChat:
    def __init__(self, linkedin_dict):
        
        self.config_num = str(random.randint(0,1000))

        os.environ["GOOGLE_API_KEY"] = 'AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q'
        self.chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        self.linkedin_content = str(linkedin_dict)  


        self.messages_history = ChatMessageHistory()
        self.stored_messages = []
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                You have solid grammer and formal writing skills and always think from recruiter's point of view.
                You have access to chat history and a LinkedIn profile section's content dictionary with keys as 
                section name and values as content written in this section. (Note: Featured section content is a summary of the content not the actual content written on linkedIn).
                
                Act as a recruiter providing expert LinkedIn profile feedback. 
                Analyze the given profile content, identify strengths, weaknesses, and suggestions tailored to the given profile. 
                Offer concise, actionable advice to enhance the profile's impact. 
                Provide general career advice as needed.
                
                Note: If user asked a general question, answer it from your knowledge. Always remember, you think as recruiter.                
                Here is the LinkedIn profile content: {linkedIn_profile} 
                 
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
                    Distill the above chat messages into a single summary message. 
                    Include as many specific details as you can related to linkedIn profile content, your revised feedback and person's background.
                    Try to be coincise and avoid redundancy.
                    Don't be distracted with irrelevant content.  
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
                    Assume the role of a seasoned recruiter with expert writing and grammar skills. 
                    Analyze the provided LinkedIn profile and chat history to optimize the profile's content. 
                    Return a modified LinkedIn profile dictionary, incorporating insights from the chat history while preserving the "person_name" key's value as it is and rewrite the other values if that is effecient.
                    reserve the keys of your returned json and the same input keys to you.
                    
                    Chat history: {chat_history}.
                    """ 
                ),("human","{linkedIn_profile}")
            ]
        )

        self.updating_chain = self.update_linkedin_prompt | self.chat
        
        self.updated_linkedin_dictionary = self.updating_chain.invoke({"chat_history":self.stored_messages,
                                                           "linkedIn_profile":old_linkedin_dict}).content
        return self.updated_linkedin_dictionary