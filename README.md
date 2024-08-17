# Chat_With_LinkedIn
## 📕 Overview:
This project aims to improve people's LinkedIn profiles and resumes using artificial intelligence. It will:
1. offer suggestions on how to strengthen your LinkedIn profile.
2. Help you create a professional resume tailored to your given job description.
![image](https://github.com/user-attachments/assets/bf975c97-196a-4193-bc17-709ca864536f)
_______________________________
## 📕 Project Goal:

To create an AI-powered tool that enhances LinkedIn profiles and generates tailored resumes based on user input and LinkedIn data.
________________
## 📕 Technical Implementation:

* ### Foundation Model:
  The project was built on top of the `Gemini-1.5-flash` model API.
* ### Core Components:
  - **LinkedIn-Content-Aware LLM:** Interacts with users to provide LinkedIn profile improvement suggestions.
  - **Resume-Aware LLM:** Help creating resumes based on user-provided job descriptions.
* ### Data Processing:
    - Person's data is scraped from LinkedIn profile using `Selenium`, `ChromeDriver`, and `BeautifulSoup`.
    - Extracted information is structured into JSON format.
* ### Model Workflow:
    - The JSON data is used to prompt engineer the `gemini-1.5-flash` model for specific tasks used in the three directories (`scrappers`, `linkedin_chatbot` and `resume_builder`).
    - Langchain is employed to create LLM chains for conversation flow and resume generation.
* ### Deployment:
    - The GUI was designed using `streamlit` 
    - The final application was containerized by building a **linux-based docker-image** [here 🐋](https://hub.docker.com/u/omarallam22).
________________

