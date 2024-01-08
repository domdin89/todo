# pull the official base image
FROM python:3.9

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt

# copy project
COPY . /app

EXPOSE 80
STOPSIGNAL SIGTERM
CMD ["sh", "./start-server.sh"]

