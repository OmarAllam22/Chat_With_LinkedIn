# Chat_With_LinkedIn
## 📕 Overview:
This project aims to improve people's LinkedIn profiles and resumes using artificial intelligence. It will:
- 1️⃣ offer suggestions on how to strengthen your LinkedIn profile.
- 2️⃣ Help you create a professional resume tailored to your given job description.

<p align="center">
 <img width="700" src="https://github.com/user-attachments/assets/ee027085-cae4-42b2-852a-6d3e6d2affdb" alt="App">
 </p>
 
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
## 📕 How to use (You have 2 choices):

### First, cloning the repository:
   * 1️⃣ run `git clone https://github.com/OmarAllam22/Chat_With_LinkedIn.git`
   * 2️⃣ open the Chat_With_LinkedIn directory & run `pip install requirements.txt`
   * 3️⃣ run `streamlit run app.py`
-------------
### Second, using the docker image (currently for linux-based os):
   * 1️⃣ From your local machine's terminal, **run `xhost +`**.
      - This step makes your machine's X-server open to connections from any host (as we want to connect this server (located on your local machine) from inside the docker container).
      - This X-server is enabled for applications that needs to run GUI from inside docker container (as docker containers is mainly CLI-based).  
   * 2️⃣ From terminal, **run `docker run -it -v /tmp/.X11-unix:/tmp/.X11-unix:ro -e DISPLAY=$DISPLAY -p 80:8501 --name app omarallam22/linkedin_chatbot:latest`**
      - This `-v /tmp/.X11-unix:/tmp/.X11-unix:ro` This mounts the local **/tmp/.X11-unix** directory to the container's **/tmp/.X11-unix** directory in **read-only** mode. This is typically used for running graphical applications within the container (GoogleChrome in our case).
      - This `-p 80:8501` maps port 8501 inside the container (default port for streamlit) to port 80 on the local host machine (default port for localhost).
   * 3️⃣ From your local machine, open a any web browser tab and **search for `http://localhost`**.
________________
## 📕 Resources:

* Hands on LangChain tutorials. [Here](https://python.langchain.com/v0.2/docs/tutorials/)
* Docker By Ahmed Sami. [Here](https://www.youtube.com/watch?v=PrusdhS2lmo&t=4310s)
* Building GUI application with docker introducing `X-server` concept. [Here](https://www.youtube.com/watch?v=cMsIT2otEjA&t=368s)
* Guide to building streamlit chatbot. [Here](https://docs.streamlit.io/develop/tutorials/llms/build-conversational-apps)
* About `streamlit.session_state` concept. [Here](https://docs.streamlit.io/get-started/fundamentals/advanced-concepts) 
* Using chromedriver and selenium on linux. [Here](https://www.youtube.com/watch?v=67h3IT2lm40)
________________
