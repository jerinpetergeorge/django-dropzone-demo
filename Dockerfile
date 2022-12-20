FROM python:3.10-slim-buster

LABEL maintainer="Jerin Peter George <jerinpetergeorge@gmail.com>"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set work directory called `app`
RUN mkdir -p /app
WORKDIR /app

# Copy local project
COPY . /app/

# Install dependencies
RUN pip install pip -U && pip install --no-cache-dir -r requirements.txt -U
