# base image
FROM python:3.10

# set env variable
ENV DockerHOME=/home/app/webapp

# set work directory
RUN mkdir -p $DockerHOME

# where is the code
WORKDIR $DockerHOME

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

# Install system dependencies
RUN apt-get update \
    && apt-get install -y postgresql-client \
    && apt-get clean

# install dependencies  
RUN pip install --upgrade pip

# copy whole project to your docker home directory. 
COPY . $DockerHOME

# run this command to install all dependencies  
RUN pip install -r requirements.txt 

# port where the Django app runs  
#EXPOSE 8000 

#CMD python manage.py runserver 0.0.0.0:8000