FROM --platform=$BUILDPLATFORM python:3.10 AS builder
EXPOSE 8000
WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . /app
