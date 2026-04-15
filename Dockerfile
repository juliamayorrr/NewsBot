FROM python:3.13-alpine

WORKDIR /bot

COPY requirements.txt ./

RUN pip install -r requirements.txt