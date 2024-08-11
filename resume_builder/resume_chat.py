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
        self.stored_messages = ChatMessageHistory()
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
                You have solid grammer and formal writing skills and always think from recruiter's point of view.
                Your task is to help a person building his/her resume via conversation and remember each time to tailor the resume content to the specific job description given to you.
                You have access to chat history and a LinkedIn profile section's content.

                Your task is to update this linkedIn profile sections if necessary to output a json with the same keys given to you.
                
                Note: If user asked a general question, answer it from your knowledge but tell him to return to the main point of building the resume tailored to the given job descriptoin.
                Always remember, you think as recruiter who filter applicants based on goodness of their resume.                
                Remeber to be coincise in your response.
                Here is the LinkedIn profile content {linkedIn_profile} 
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
                    Include as many specific details as you can.
                    Don't forget each time to keep information in your summary about the linkedIn profile content and the person's background and try to make the summary be coincise and long as information needs not repetitive.
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
                    You have solid grammer and formal writing skills and always think from recruiter's point of view.
                    Your task is to:
                    - take a json contains linkedIn profile content for a given person.
                    - return a json with the same keys but the values enhanced and improved from the chat and conversation history. (ex: analyzing the messages history may give intuition to change some values of the dictionary and may not).
                    Note (the person name key isn't changed anymore).
                    return your answer as json dictionary.
                    This is the messages history: {chat_history}.
                    """ 
                ),("human","{linkedIn_profile}")
            ]
        )

        self.updating_chain = self.update_linkedin_prompt | self.chat
        
        self.updated_linkedin_dictionary = self.updating_chain.invoke({"chat_history":self.stored_messages,
                                                           "linkedIn_profile":old_linkedin_dict}).content
        return self.updated_linkedin_dictionary