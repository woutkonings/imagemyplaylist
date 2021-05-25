FROM bo3s/pandas_numpy:3.9.5

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
