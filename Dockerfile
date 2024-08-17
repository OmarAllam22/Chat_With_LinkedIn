# getting the base image
FROM python:3.9-slim-buster
# creating a directory for the app
WORKDIR /app
# copying the git directory into docker
COPY . /app/
# RUN the script to install both google-chrome and chrome-driver
RUN chmod +x ./stuff_installation.sh
RUN ./stuff_installation.sh
#running the app
ENTRYPOINT ["/bin/bash","-c"]
CMD streamlit run app.py