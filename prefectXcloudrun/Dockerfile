FROM python:3.9

RUN apt-get update

RUN apt-get install curl

RUN curl -sSL https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN curl -sSL -o /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$(curl -sS http://chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99
##############################################################

COPY pipeline.py /opt/prefect/flows/pipeline.py

RUN mkdir /opt/prefect/flows/data/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /opt/prefect/flows/
