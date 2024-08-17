# getting the base image
FROM python:3.9-slim-buster
# copying the git directory into docker
COPY . .
# RUN the script to install both google-chrome and chrome-driver
RUN chmod +x ./stuff_installation.sh
RUN ./stuff_installation.sh
RUN pip install requirements.txt
#running the app
ENTRYPOINT ["/bin/bash","-c"]
CMD streamlit run app.py
