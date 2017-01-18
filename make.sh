#!/bin/bash

#make sure pip is installed
sudo easy_install pip

#make sure virtualenv is installed
sudo pip install virtualenv
sudo pip install --upgrade virtualenv

#Create virtual environment .env
virtualenv .env
source .env/bin/activate
pip install -r requirements.txt

#create executable
echo -e "cd $PWD\nsource .env/bin/activate\npython ngrams.py" >> run.command

#Authorize Executable
chmod u+x run.command
