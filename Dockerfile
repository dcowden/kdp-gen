FROM python:3.9.19-slim-bookwork
COPY requirements.txt /src
WORKDIR /src
apt-get update
apt-get upgrade
apt-get install ffmpeg libsm6 libxext6  -y
pip install --upgrade pip
pip install -r requirements.txt
apt-get install ttf-mscorefonts-installer
fc-cache -fv
fc-list