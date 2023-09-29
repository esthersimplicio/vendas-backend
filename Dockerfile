FROM python:latest

# Create app directory
WORKDIR /app

EXPOSE 5000

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y ncat
RUN apt-get install -y iputils-ping

# Install cryptography package
RUN pip install cryptography

# Install app dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Bundle app source
COPY . /app
