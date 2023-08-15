# This is version for development

# pull official base image
FROM python:3.10.6-alpine
# FROM python:3.10.6

# set work directory
WORKDIR /paper_management_project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies with apk (PM of apline)
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev
RUN apt-get update && apt-get -y dist-upgrade
RUN apt-get install -y netcat

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# run server
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000"]