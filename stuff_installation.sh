#!/bin/bash
#install google-chrome
apt-get update
yes | apt-get upgrade
yes | apt install wget
yes | wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
yes | apt --fix-broken install
dpkg -i google-chrome-stable_current_amd64.deb
# install chrome-driver
wget https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.119/linux64/chromedriver-linux64.zip
apt-get install unzip
unzip chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver
mv chromedriver-linux64/chromedriver /usr/local/share/chromedriver
ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver
ln -s /usr/local/share/chromedriver /usr/bin/chromedriver
# adding new_user(to open chrome as non-root user)
useradd new_user
su new_user
bash
