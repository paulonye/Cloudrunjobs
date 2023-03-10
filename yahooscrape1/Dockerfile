FROM python:3.8

##################################################
#The following steps configures the setup of 
#google chrome and the chrome driver

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99
##############################################################

#Copies the service account key into the docker container
COPY key.json /home/app/key.json

#Sets the service account key.json as an environmental variable called key_file
ENV key_file key.json

#Copies the needed libraries 
COPY requirements.txt /home/app/requirements.txt

#Installs the needed libraries
RUN pip install -r /home/app/requirements.txt

#Copies the ff scripts into the docker container
COPY connect.py /home/app/connect.py
COPY main.py /home/app/main.py
COPY scrape.py /home/app/scrape.py

#Sets the working directory
WORKDIR /home/app

ENTRYPOINT ["python", "/home/app/main.py"]
#This is the default argument for the google sheet and the sheet that
#you are pushing the data to
#change to reflect yours
CMD ["--googlesheet", "test_sheet", "--sheetname", "data4"]