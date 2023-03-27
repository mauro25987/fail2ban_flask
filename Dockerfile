FROM python:3.8-alpine

RUN apk add --no-cache bash openssh-client

RUN mkdir /root/.ssh

COPY keys/* /root/.ssh/

ADD . /app

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt
