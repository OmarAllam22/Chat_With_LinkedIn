from langchain_google_genai import ChatGoogleGenerativeAI
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyDzyMWZB82YyWKzf21k6qdiAn4JG6DXL-Q"
model = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.2 # if the model makes decisions, use lower temperature 