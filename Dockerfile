# syntax=docker/dockerfile:1
FROM python:3.8-slim
ENV PATH /usr/local/bin:$PATH
RUN apt-get update && apt-get install build-essential libpq-dev python-dev -y
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /chatbot
COPY requirements.txt /chatbot/
RUN pip3 install psycopg2-binary && pip3 install -r requirements.txt
COPY . /chatbot/
CMD [ "python3", "manage.py", "migrate"]
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]
