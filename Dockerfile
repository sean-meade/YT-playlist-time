# syntax=docker/dockerfile:1
FROM ubuntu:18.04
RUN apt -f install -y
RUN apt-get install -y wget
RUN apt install chromium-browser
RUN apt-get install -y chromium-browser

FROM python:3.8-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]