FROM python:3.8.9

WORKDIR /usr/src/app

COPY ./* ./
RUN apt-get update -yqq \
    	&& apt-get upgrade -yqq \
    	&& apt-get install -yqq --no-install-recommends \
        libpq-dev\
        python3-dev\
        gcc\
        curl
RUN pip install --no-cache-dir -r requirements.txt
RUN export FLASK_APP=flaskr
