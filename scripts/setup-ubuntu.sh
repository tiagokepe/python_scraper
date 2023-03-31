#!/bin/bash

sudo pip3 install -r requirements.txt && mkdir -p log/screenshots

export DEBIAN_FRONTEND=noninteractive
export TZ=Europe/Madrid
sudo apt-get install wget -y
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome*.deb  -y
