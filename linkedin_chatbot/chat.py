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
        self.chat = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
        self.linkedin_content = str(linkedin_dict)  


        self.messages_history = ChatMessageHistory()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system", """
                You have solid grammer and formal writing skills and always think from recruiter's point of view.
                You have access to chat history and a LinkedIn profile section's content dictionary with keys as 
                section name and values as content written in this section. (Note: Featured section content is a summary of the content not the actual content written on linkedIn).
                Your task is to answer the user queries to enhance the linkedIn profile sections content given to you, for example you may:
                - recommend adding missing sections.
                - correct the given sections if they are written grammatically wrong or formally wrong.
                - strenthen the given content to be outstanding from a recruiter point of view.
                Note: If user asked a general question, answer it from your knowledge. Always remember, you think as recruiter.                
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
                    Don't forget each time to keep information in your summary about the linkedIn profile content and the person background.  
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
