FROM python:3.7-slim

RUN apt-get update && \
    apt-get -y install \
    gcc \
    python3-dev

COPY ../app/backend/pip/requirements.txt /var/app/pip/requirements.txt

RUN pip3 install -r /var/app/pip/requirements.txt

COPY ../app/backend/ /var/app/

WORKDIR /var/app/src/

EXPOSE 8000
